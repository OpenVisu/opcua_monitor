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

from asyncua import Server
import unittest
from monitor import Monitor


class TestMain(unittest.IsolatedAsyncioTestCase):
    server: Server

    url: str = "opc.tcp://0.0.0.0:4842/"

    async def asyncSetUp(self):
        self.server = Server()
        await self.server.init()
        self.server.set_endpoint(self.url)
        await self.server.start()

    async def test_connection_successful(self):
        status = await Monitor.test_connection(self.url)
        self.assertEqual(status, '')

    async def test_connection_fail(self):
        status = await Monitor.test_connection("opc.tcp://0.0.0.0:4843/")
        self.assertEqual(status, 'OSError')

    async def asyncTearDown(self):
        await self.server.stop()
