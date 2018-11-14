import socket

from dns import resolver
from dns.resolver import NoAnswer


def find_root_cname(url: str):
    loop = True
    while loop:
        try:
            url = resolver.query(url, 'CNAME')[0].to_text()
        except NoAnswer:  # We have reached the bottom of the CNAME chain
            loop = False
    return url


def reverse_dns(ip: str):
    try:
        url = socket.gethostbyaddr(ip)[0]
        return url
    except socket.herror:  # No result
        return ''
