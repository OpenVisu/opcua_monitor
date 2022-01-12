#!/usr/local/bin/python3
# Copyright (C) 2022 Robin Jespersen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import os
from concurrent.futures import CancelledError

import time
from opcua import Client
from opcua.ua import UaError
from opcua.ua.uaerrors import BadTooManySessions
from sentry_sdk import start_transaction

import sentry_sdk

from backend import Backend

if os.getenv('SENTRY_DSN') is not None:
    sentry_sdk.init(
        os.getenv('SENTRY_DSN'),
        traces_sample_rate=os.getenv('SENTRY_TRACES_SAMPLE_RATE', 1),
    )

backend: Backend = Backend(
    os.getenv('API_URL', 'http://api/'),
    os.environ['ACCESS_TOKEN'],
)

if __name__ == '__main__':
    # if a successful connection was made in the last update_interval
    # seconds don't try again
    update_interval = 60

    while True:

        with start_transaction(op="loop", name='loop'):
            check_time = int(time.time())
            check_datetime = datetime.datetime.fromtimestamp(
                check_time, tz=datetime.timezone.utc)

            servers = backend.server_index()

            opcua_client: Client

            for server in servers:
                opcua_client = Client(server['url'], timeout=10)
                opcua_client.session_timeout = 1000
                opcua_client.secure_channel_timeout = 300000
                connected = False
                connection_error = ''
                try:
                    opcua_client.connect()
                    connected = True
                    opcua_client.disconnect()
                except CancelledError:
                    connection_error = 'CancelledError'
                except OSError:
                    connection_error = 'OSError'
                except UaError:
                    connection_error = 'UaError'
                backend.server_update(server['id'], connection_error)

        # TODO might be a good idea to clean up orphaned nodes and endpoints here

        time.sleep(update_interval)
