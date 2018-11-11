import os

from aiohttp import web

listen_port = int(os.getenv("LISTEN_PORT", 8080))


async def detect_cdns(request):
    json = await request.json()
    return web.json_response(json)


def setup_app():
    app = web.Application()
    app.router.add_get('/', detect_cdns)
    return app


def run_app(port):
    app = setup_app()
    web.run_app(app, port=port)


if __name__ == "__main__":
    run_app(listen_port)
