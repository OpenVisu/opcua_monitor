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

import time
import requests


class Backend:
    API_URL: str
    ACCESS_TOKEN: str

    def __init__(self, api_url: str, access_token: str):
        self.API_URL = api_url
        self.ACCESS_TOKEN = access_token

    def available(self) -> bool:
        response = requests.get(
            self.API_URL + '/api/status/ping',
        )
        return response.status_code == 200

    def server_index(self):
        response = requests.get(
            self.API_URL + '/api/server_manager/server/index',
            headers=self._get_headers(),
        )
        return response.json()

    def server_update(self, server_id: int, connection_error: str = ''):
        checked_at: int = round(time.time() + 5)  # hack

        data = {
            'checked_at': checked_at,
        }
        if connection_error == '':
            data['has_connection_error'] = 0
            data['connection_error'] = ''
        else:
            data['has_connection_error'] = 1
            data['connection_error'] = connection_error

        requests.patch(
            self.API_URL + '/api/server_manager/server/update?id=%s' % server_id,
            headers=self._get_headers(),
            data=data,
        )

    def _get_headers(self):
        return {"Authorization": "Bearer %s" % self.ACCESS_TOKEN}
