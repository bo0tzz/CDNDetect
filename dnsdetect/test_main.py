from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
import dnsdetect.main
import unittest


class TestCase(AioHTTPTestCase):

    async def get_application(self):
        return dnsdetect.main.setup_app()

    @unittest_run_loop
    async def test_hello_world(self):
        resp = await self.client.request("GET", "/")
        assert resp.status == 200
        text = await resp.text()
        print(text)
        assert "Hello World" == text


if __name__ == '__main__':
    unittest.main()

