import asyncio
import os

from aiohttp import web

import chrome
import detect


class Main:

    def __init__(self):
        self.listen_port = int(os.getenv("LISTEN_PORT", 8080))
        self.browser = None
        self.app = None
        self.detect = detect.Detect()

    async def detect_cdns(self, request):
        results = {}

        request_json = await request.json()
        url = request_json['url']

        # Find the resources on the webpage
        resp = await self.browser.find_resources(url)

        for domain in resp:
            cdn = self.detect.find_cdn(domain)
            results[domain] = cdn

        return web.json_response(results)

    async def setup_app(self):

        self.browser = chrome.Chrome()
        await self.browser.setup()

        self.app = web.Application()
        self.app.router.add_get('/', self.detect_cdns)


if __name__ == "__main__":
    m = Main()
    asyncio.get_event_loop().run_until_complete(m.setup_app())
    web.run_app(m.app, port=m.listen_port)
