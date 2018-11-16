from dnsdetect import detect
from parameterized import parameterized
import unittest


class TestDetect(unittest.TestCase):

    @parameterized.expand([
        ['assets.funnygames.at', 'd.gcdn.co.'],
        ['edition.i.cdn.cnn.com', 'turner-tls.map.fastly.net.'],
        ['cdn.cnn.com', 'e12596.dscj.akamaiedge.net.']
    ])
    def test_cname_chain(self, base_url, expected):
        root_cname = detect.find_root_cname(base_url)
        self.assertEqual(expected, root_cname)

    @parameterized.expand([
        ['54.230.129.171', 'server-54-230-129-171.ams50.r.cloudfront.net']  # TODO: Find more relevant test cases
    ])
    def test_reverse_dns(self, ip, expected):
        url = detect.reverse_dns(ip)
        self.assertEqual(expected, url)

    @parameterized.expand([
        ['www.funnygames.at', True],
        ['static.ah.nl', True],
        ['images.nrc.nl', True],
        ['www.cloudflare.com', True],
        ['www.warpcache.com', False],
        ['www.google.com', False],
        ['www.tweakers.net', False]
    ])
    def test_detect_cloudflare(self, url, is_cloudflare):
        res = detect.detect_cloudflare(url)
        self.assertEqual(is_cloudflare, res)

if __name__ == '__main__':
    unittest.main()

