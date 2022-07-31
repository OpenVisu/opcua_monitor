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

from concurrent.futures import CancelledError

from asyncua import Client
from asyncua.ua import UaError


class Monitor:
    @staticmethod
    async def test_connection(url: str) -> str:
        """
        :param url: url of the server.
        test if it is possible to connect to the server
        """
        opcua_client = Client(url, timeout=10)
        opcua_client.session_timeout = 1000
        opcua_client.secure_channel_timeout = 300000
        connection_error = ''
        try:
            await opcua_client.connect()
            await opcua_client.disconnect()
        except CancelledError:
            connection_error = 'CancelledError'
        except OSError:
            connection_error = 'OSError'
        except UaError:
            connection_error = 'UaError'
        return connection_error
