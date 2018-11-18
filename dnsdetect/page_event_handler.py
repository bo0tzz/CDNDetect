from urllib import parse


class PageEventHandler:

    def __init__(self):
        self.requested = set()

    def handle_event(self, event):
        parsed = parse.urlparse(event.url)
        self.requested.add(parsed.netloc)

