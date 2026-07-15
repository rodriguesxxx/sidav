import pytest
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from server.routes import create_app


class TestRoutes(AioHTTPTestCase):

    async def get_application(self):
        return create_app()

    @unittest_run_loop
    async def test_index_returns_200(self):
        resp = await self.client.get("/")
        assert resp.status == 200

    @unittest_run_loop
    async def test_ping_returns_pong(self):
        resp = await self.client.get("/api/ws/ping")
        assert resp.status == 200
        text = await resp.text()
        assert text == "pong"

    @unittest_run_loop
    async def test_ws_cam_endpoint_exists(self):
        resp = await self.client.ws_connect("/api/ws/cam")
        assert not resp.closed
        await resp.close()

    @unittest_run_loop
    async def test_ws_serial_endpoint_exists(self):
        resp = await self.client.ws_connect("/api/ws/serial")
        assert not resp.closed
        await resp.close()