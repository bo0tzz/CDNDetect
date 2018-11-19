import asyncio
import os
import sys

from aiohttp import web

from dnsdetect.browser import Browser
from dnsdetect.detect import Detect


class Main:

    def __init__(self, listen_port):
        self.listen_port = listen_port
        self.browser = None
        self.app = None
        self.detect = Detect()

    async def detect_cdns(self, request):
        results = {}

        request_json = await request.json()
        url = request_json['url']

        # Find the resources on the webpage
        resp = await self.browser.find_resources(url)

        for domain in resp:
            cdn = self.detect.find_cdn(domain)
            if cdn != '':
                results[domain] = cdn

        return web.json_response(results)

    async def setup_app(self):

        self.browser = Browser()
        await self.browser.setup()

        self.app = web.Application()
        self.app.router.add_get('/', self.detect_cdns)


if __name__ == "__main__":
    port = int(sys.argv[1]) \
        if len(sys.argv) > 1 \
        else int(os.getenv("LISTEN_PORT", 8080))

    m = Main(port)
    asyncio.get_event_loop().run_until_complete(m.setup_app())
    web.run_app(m.app, port=m.listen_port)
