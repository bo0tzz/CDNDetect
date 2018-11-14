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


if __name__ == '__main__':
    unittest.main()

