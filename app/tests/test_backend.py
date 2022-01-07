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

from backend import Backend
import httpretty
import unittest


class TestBackend(unittest.TestCase):
    backend: Backend

    def setUp(self):
        self.backend = Backend('http://test-server', 'test-token')

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_available(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://test-server/api/status/ping',
            status=200
        )
        self.assertTrue(self.backend.available())

        httpretty.register_uri(
            httpretty.GET,
            'http://test-server/api/status/ping',
            status=404
        )
        self.assertFalse(self.backend.available())

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_server_index(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://test-server/api/server_manager/server/index',
            status=200,
        )
        servers = self.backend.server_index()
        latest: httpretty.core.HTTPrettyRequest = httpretty.latest_requests()[
            0]
        self.assertEqual(latest.headers['Authorization'], 'Bearer test-token')

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_server_update(self):
        httpretty.register_uri(
            httpretty.PATCH,
            'http://test-server/api/server_manager/server/update',
            status=200,
        )
        self.backend.server_update(5, 'some error')
        latest: httpretty.core.HTTPrettyRequest = httpretty.latest_requests()[
            0]
        self.assertTrue('checked_at=' in str(latest.body))
        self.assertTrue(
            '&has_connection_error=1&connection_error=some+error' in str(latest.body))
        self.assertEqual(latest.querystring['id'][0], '5')


if __name__ == '__main__':
    unittest.main()
