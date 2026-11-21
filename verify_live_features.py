import urllib.request

article_url = 'https://ainews-krishnavibez.web.app/articles/openai-o3-reasoning-breakthrough-system-2-thinking.html'
req = urllib.request.Request(article_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8')
    print('Reading Progress Bar:', 'readingProgress' in html)
    print('Table of Contents (TOC):', 'article-toc' in html)
    print('Author Bio Card:', 'author-bio-card' in html)
    print('Section 1 Jump Anchor (#breakthrough):', 'id="breakthrough"' in html)

key_url = 'https://ainews-krishnavibez.web.app/e4c8b21a97d54930ba81f182c6de3421.txt'
with urllib.request.urlopen(urllib.request.Request(key_url, headers={'User-Agent': 'Mozilla/5.0'})) as res:
    print('IndexNow Key HTTP:', res.status, '| Key Content:', res.read().decode('utf-8').strip())

root_url = 'https://krishna-vibez.web.app/'
with urllib.request.urlopen(urllib.request.Request(root_url, headers={'User-Agent': 'Mozilla/5.0'})) as res:
    root_html = res.read().decode('utf-8')
    print('Root Portal Backlink to AINews present:', 'ainews.krishnavibez.in' in root_html)
