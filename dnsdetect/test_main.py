import json
import unittest

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

import dnsdetect.main


class TestMain(AioHTTPTestCase):

    async def get_application(self):
        return dnsdetect.main.setup_app()

    @unittest_run_loop
    async def test_funnygames_at(self):
        rq = {'url': 'https://www.funnygames.at/'}
        resp = await self.client.request("GET", "/", data=(json.dumps(rq)))
        assert resp.status == 200
        resp_json = await resp.json()
        assert len(resp_json) == 2
        assert resp_json['www.funnygames.at'] == 'Cloudflare'
        # The example in the email specifies OptimiCDN, but this seems to be a multi-CDN.
        # Locally I am routed onto the G-core labs CDN. This test may fail in other locations.
        assert resp_json['assets.funnygames.at'] == 'G-core'

    @unittest_run_loop
    async def test_warpcache_com(self):
        rq = {'url': 'https://www.warpcache.com/'}
        resp = await self.client.request("GET", "/", data=(json.dumps(rq)))
        assert resp.status == 200
        resp_json = await resp.json()
        assert len(resp_json) == 0  # No CDN used

    @unittest_run_loop
    async def test_edition_cnn_com(self):
        rq = {'url': 'https://edition.cnn.com/'}
        resp = await self.client.request("GET", "/", data=(json.dumps(rq)))
        assert resp.status == 200
        resp_json = await resp.json()
        assert len(resp_json) == 2
        assert resp_json['edition.i.cdn.cnn.com'] == 'Fastly'
        assert resp_json['cdn.cnn.com'] == 'Akamai'

    @unittest_run_loop
    async def test_thuisbezorgd_nl(self):
        rq = {'url': 'https://www.thuisbezorgd.nl'}
        resp = await self.client.request("GET", "/", data=(json.dumps(rq)))
        assert resp.status == 200
        resp_json = await resp.json()
        assert len(resp_json) == 1
        assert resp_json['www.thuisbezorgd.nl'] == 'Fastly'

    @unittest_run_loop
    async def test_dell_com(self):
        rq = {'url': 'https://www.dell.com'}
        resp = await self.client.request("GET", "/", data=(json.dumps(rq)))
        assert resp.status == 200
        resp_json = await resp.json()
        assert len(resp_json) == 2
        assert resp_json['www.dell.com'] == 'Akamai'
        assert resp_json['i.dell.com'] == 'Akamai'

    @unittest_run_loop
    async def test_youtube_com(self):
        rq = {'url': 'https://www.youtube.com'}
        resp = await self.client.request("GET", "/", data=(json.dumps(rq)))
        assert resp.status == 200
        resp_json = await resp.json()
        assert len(resp_json) == 1
        assert resp_json['www.youtube.com'] == 'Google'

    @unittest_run_loop
    async def test_ah_nl(self):
        rq = {'url': 'https://www.ah.nl'}
        resp = await self.client.request("GET", "/", data=(json.dumps(rq)))
        assert resp.status == 200
        resp_json = await resp.json()
        assert len(resp_json) == 1
        assert resp_json['static.ah.nl'] == 'Cloudflare'

    @unittest_run_loop
    async def test_buienradar_nl(self):
        rq = {'url': 'https://www.buienradar.nl'}
        resp = await self.client.request("GET", "/", data=(json.dumps(rq)))
        assert resp.status == 200
        resp_json = await resp.json()
        assert len(resp_json) == 4
        assert resp_json['static.buienradar.nl'] == 'Akamai'
        assert resp_json['api.buienradar.nl'] == 'Akamai'
        assert resp_json['graphdata.buienradar.nl'] == 'Akamai'
        assert resp_json['forecast.buienradar.nl'] == 'Akamai'

    @unittest_run_loop
    async def test_coolblue_nl(self):
        rq = {'url': 'https://www.coolblue.nl'}
        resp = await self.client.request("GET", "/", data=(json.dumps(rq)))
        assert resp.status == 200
        resp_json = await resp.json()
        assert len(resp_json) == 3
        assert resp_json['image.coolblue.nl'] == 'Amazon Cloudfront'
        assert resp_json['assets.coolblue.nl'] == 'Amazon Cloudfront'
        assert resp_json['www.coolblue.nl'] == 'Amazon Cloudfront'

    @unittest_run_loop
    async def test_nrc_nl(self):
        rq = {'url': 'https://www.nrc.nl'}
        resp = await self.client.request("GET", "/", data=(json.dumps(rq)))
        assert resp.status == 200
        resp_json = await resp.json()
        assert len(resp_json) == 1
        assert resp_json['images.nrc.nl'] == 'Cloudflare'


if __name__ == '__main__':
    unittest.main()
