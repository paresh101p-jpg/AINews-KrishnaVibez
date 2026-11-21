import urllib.request
import json

payload = {
    "host": "ainews.krishnavibez.in",
    "key": "e4c8b21a97d54930ba81f182c6de3421",
    "keyLocation": "https://ainews.krishnavibez.in/e4c8b21a97d54930ba81f182c6de3421.txt",
    "urlList": [
        "https://ainews.krishnavibez.in/",
        "https://ainews.krishnavibez.in/articles/openai-o3-reasoning-breakthrough-system-2-thinking.html",
        "https://ainews.krishnavibez.in/authors/paresh-padsala.html",
        "https://ainews.krishnavibez.in/about.html"
    ]
}

data = json.dumps(payload).encode("utf-8")
headers = {"Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0"}

for endpoint in ["https://api.indexnow.org/indexnow", "https://www.bing.com/indexnow"]:
    req = urllib.request.Request(endpoint, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"{endpoint} -> Status: {resp.status} (SUCCESS)")
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", errors="ignore")
        print(f"{endpoint} -> HTTP {e.code}: {msg}")
    except Exception as e:
        print(f"{endpoint} -> Error: {e}")
