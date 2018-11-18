from pyppeteer import launch

from page_event_handler import PageEventHandler


class Chrome:

    def __init__(self):
        self.browser = None

    async def setup(self):
        self.browser = await launch()

    async def find_resources(self, url):
        handler = PageEventHandler()
        page = await self.browser.newPage()
        page.on('request', handler.handle_event)

        await page.goto(url)
        return handler.requested
