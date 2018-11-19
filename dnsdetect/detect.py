import json
import socket
import requests

from dns import resolver
from dns.resolver import NoAnswer
import ipaddress


def compare_domains(cname: str, domain: str):
    if cname.endswith('.'):
        cname = cname.rstrip('.')

    if domain.endswith('.'):  # If our cdn domain ends in '.', that cdn uses most TLDs
        domain = domain.rstrip('.')
        cname = cname[0: cname.rindex('.')]  # So we snip the TLD off our url before comparing

    return cname.endswith(domain)


def reverse_dns(ip: str):
    try:
        url = socket.gethostbyaddr(ip)[0]
        return url
    except socket.herror:  # No result
        return ''


def find_root_cname(url: str):
    loop = True
    while loop:
        try:
            url = resolver.query(url, 'CNAME')[0].to_text()
        except NoAnswer:  # We have reached the bottom of the CNAME chain
            loop = False
    return url


def ip_from_url(url):
    ip = resolver.query(url, 'A')[0].to_text()
    return ip


class Detect:

    def __init__(self):
        # Load CDN domains
        with open('cdn.json') as f:
            self.cdns = json.load(f)

        # Load cloudflare ranges
        self.cloudflare_ranges = []
        r = requests.get('https://cloudflare.com/ips-v4')
        for line in r.text.split('\n'):
            if line != '':
                self.cloudflare_ranges.append(line)

    def detect_cloudflare(self, url: str):
        # Find the IP for this url
        ip = ip_from_url(url)
        is_cloudflare = False
        ip_addr = ipaddress.ip_address(ip)

        # See if the ip is a cloudflare ip
        for r in self.cloudflare_ranges:
            if ip_addr in ipaddress.ip_network(r):
                is_cloudflare = True
        return is_cloudflare

    def find_cdn(self, url: str):
        cname = find_root_cname(url)
        # If there is no cname chain, let's see if the resource is on cloudflare
        if cname == url:
            if self.detect_cloudflare(url):
                return 'Cloudflare'
            else:
                ip = ip_from_url(url)
                cname = reverse_dns(ip)
                if cname == '':
                    return ''

        # See if the root cname is in our list of CDN domains
        for domain, cdn in self.cdns.items():
            if compare_domains(cname, domain):
                return cdn

        return ''
