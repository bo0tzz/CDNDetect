from dnsdetect import detect
import unittest


class TestDetect(unittest.TestCase):

    def test_funnygames_at(self):
        base_url = 'assets.funnygames.at'
        root_cname = detect.find_root_cname(base_url)
        self.assertEqual('d.gcdn.co.', root_cname)

    def test_edition_cnn_com(self):
        base_url = 'edition.i.cdn.cnn.com'
        root_cname = detect.find_root_cname(base_url)
        self.assertEqual('turner-tls.map.fastly.net.', root_cname)

    def test_cdn_cnn_com(self):
        base_url = 'cdn.cnn.com'
        root_cname = detect.find_root_cname(base_url)
        self.assertEqual('e12596.dscj.akamaiedge.net.', root_cname)


if __name__ == '__main__':
    unittest.main()

