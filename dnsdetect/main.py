from aiohttp import web
import os

listen_port = int(os.getenv("LISTEN_PORT", 8080))


async def detect_cdns(request):
    return web.Response(text="Hello World")


def setup_app():
    app = web.Application()
    app.router.add_get('/', detect_cdns)
    return app


def run_app(port):
    app = setup_app()
    web.run_app(app, port=port)


if __name__ == "__main__":
    run_app(listen_port)
