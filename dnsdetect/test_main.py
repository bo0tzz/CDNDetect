import json
import unittest

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

import dnsdetect.main


class TestMain(AioHTTPTestCase):

    async def get_application(self):
        main = dnsdetect.main.Main(8080)
        await main.setup_app()
        return main.app

    async def make_request(self, rq):
        resp = await self.client.request("GET", "/", data=(json.dumps(rq)))
        assert resp.status == 200
        return await resp.json()

    @unittest_run_loop
    async def test_funnygames_at(self):
        rq = {'url': 'https://www.funnygames.at/'}
        resp_json = await self.make_request(rq)
        assert len(resp_json) == 2
        assert resp_json['www.funnygames.at'] == 'Cloudflare'
        # The example in the email specifies OptimiCDN, but this seems to be a multi-CDN.
        # Locally I am routed onto the G-core labs CDN. This test may fail in other locations.
        assert resp_json['assets.funnygames.at'] == 'G-core'

    @unittest_run_loop
    async def test_warpcache_com(self):
        rq = {'url': 'https://www.warpcache.com/'}
        resp_json = await self.make_request(rq)
        assert len(resp_json) == 0  # No CDN used

    @unittest_run_loop
    async def test_edition_cnn_com(self):
        rq = {'url': 'https://edition.cnn.com/'}
        resp_json = await self.make_request(rq)
        assert len(resp_json) == 4
        assert resp_json['edition.i.cdn.cnn.com'] == 'Fastly'
        assert resp_json['data.cnn.com'] == 'Akamai'
        assert resp_json['cdn.cnn.com'] == 'Akamai'
        assert resp_json['dynaimage.cdn.cnn.com'] == 'Akamai'

    @unittest_run_loop
    async def test_thuisbezorgd_nl(self):
        rq = {'url': 'https://www.thuisbezorgd.nl'}
        resp_json = await self.make_request(rq)
        assert len(resp_json) == 1
        assert resp_json['www.thuisbezorgd.nl'] == 'Fastly'

    @unittest_run_loop
    async def test_dell_com(self):
        rq = {'url': 'https://www.dell.com'}
        resp_json = await self.make_request(rq)
        assert len(resp_json) == 3
        assert resp_json['www.dell.com'] == 'Akamai'
        assert resp_json['i.dell.com'] == 'Akamai'
        assert resp_json['nexus.dell.com'] == 'Akamai'

    @unittest_run_loop
    async def test_youtube_com(self):
        rq = {'url': 'https://www.youtube.com'}
        resp_json = await self.make_request(rq)
        assert len(resp_json) == 1
        assert resp_json['www.youtube.com'] == 'Google'

    @unittest_run_loop
    async def test_ah_nl(self):
        rq = {'url': 'https://www.ah.nl'}
        resp_json = await self.make_request(rq)
        assert len(resp_json) == 1
        assert resp_json['static.ah.nl'] == 'Cloudflare'

    @unittest.skip("The buienradar website uses different resources occasionally")
    @unittest_run_loop
    async def test_buienradar_nl(self):
        rq = {'url': 'https://www.buienradar.nl'}
        resp_json = await self.make_request(rq)
        assert len(resp_json) == 2
        assert resp_json['static.buienradar.nl'] == 'Akamai'
        assert resp_json['api.buienradar.nl'] == 'Akamai'

    @unittest_run_loop
    async def test_coolblue_nl(self):
        rq = {'url': 'https://www.coolblue.nl'}
        resp_json = await self.make_request(rq)
        assert len(resp_json) == 3
        assert resp_json['image.coolblue.nl'] == 'Amazon Cloudfront'
        assert resp_json['assets.coolblue.nl'] == 'Amazon Cloudfront'
        assert resp_json['www.coolblue.nl'] == 'Amazon Cloudfront'

    @unittest_run_loop
    async def test_nrc_nl(self):
        rq = {'url': 'https://www.nrc.nl'}
        resp_json = await self.make_request(rq)
        assert len(resp_json) == 0

    @unittest_run_loop
    async def test_digitalocean_com(self):
        rq = {'url': 'https://www.digitalocean.com'}
        resp_json = await self.make_request(rq)
        assert len(resp_json) == 2
        assert resp_json['www.digitalocean.com'] == 'Cloudflare'
        assert resp_json['assets.digitalocean.com'] == 'Fastly'


if __name__ == '__main__':
    unittest.main()
