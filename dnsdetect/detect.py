import socket
import requests

from dns import resolver
from dns.resolver import NoAnswer
import ipaddress

class Detect:

    def __init__(self):
        self.cloudflare_ranges = []
        r = requests.get('https://cloudflare.com/ips-v4')
        for l in r.text.split('\n'):
            if l != '':
                self.cloudflare_ranges.append(l)

    def detect_cloudflare(self, url: str):
        url = self.find_root_cname(url)
        ip = resolver.query(url, 'A')[0].to_text()
        is_cloudflare = False
        ip_addr = ipaddress.ip_address(ip)
        print(self.cloudflare_ranges)
        for r in self.cloudflare_ranges:
            if ip_addr in ipaddress.ip_network(r):
                is_cloudflare = True
        return is_cloudflare

    def find_root_cname(self, url: str):
        loop = True
        while loop:
            try:
                url = resolver.query(url, 'CNAME')[0].to_text()
            except NoAnswer:  # We have reached the bottom of the CNAME chain
                loop = False
        return url

    def reverse_dns(self, ip: str):
        try:
            url = socket.gethostbyaddr(ip)[0]
            return url
        except socket.herror:  # No result
            return ''
