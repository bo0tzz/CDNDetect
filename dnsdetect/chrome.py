from pyppeteer import launch
from urllib import parse

from page_event_handler import PageEventHandler


class Chrome:

    def __init__(self):
        self.browser = None

    async def setup(self):
        self.browser = await launch()

    async def find_resources(self, url):
        handler = PageEventHandler()
        page = await self.browser.newPage()
        page.on('request', handler.handle_page_request_event)

        # Load the page to find the resources used
        await page.goto(url)

        # Filter resource URLs for the same domain
        (domain, tld) = parse.urlparse(url).netloc.split('.')[-2:]
        return [e for e in handler.requested if e.endswith(f"{domain}.{tld}")]
