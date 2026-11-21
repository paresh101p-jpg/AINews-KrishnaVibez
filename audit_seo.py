import urllib.request
import time
import json
import re

urls = [
    'https://ainews-krishnavibez.web.app/',
    'https://ainews-krishnavibez.web.app/articles/openai-o3-reasoning-breakthrough-system-2-thinking.html',
    'https://ainews-krishnavibez.web.app/authors/paresh-padsala.html',
    'https://ainews-krishnavibez.web.app/sitemap.xml',
    'https://ainews-krishnavibez.web.app/rss.xml'
]

print("=== SPEED & TTFB AUDIT ===")
for u in urls:
    t0 = time.time()
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            dur = (time.time() - t0) * 1000
            headers = dict(resp.headers)
            body = resp.read()
            size = len(body)
            print(f"\nURL: {u}")
            print(f"  HTTP Status: {resp.status}")
            print(f"  TTFB / Total Time: {dur:.1f} ms")
            print(f"  Page Size: {size / 1024:.2f} KB")
            print(f"  Content-Type: {headers.get('content-type', 'unknown')}")
            print(f"  Cache-Control: {headers.get('cache-control', 'none')}")
    except Exception as e:
        print(f"Error {u}: {e}")
