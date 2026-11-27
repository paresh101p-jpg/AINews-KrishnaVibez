import requests

files_map = {
    "margashirsha-krishna-hero.jpg": "/data/user/0/ai.antigem/files/home/projects/Auto-Insta-Krishna/website/public/images/articles/margashirsha-krishna-hero.jpg",
    "margashirsha-brahma-muhurta.jpg": "/data/user/0/ai.antigem/files/home/projects/Auto-Insta-Krishna/website/public/images/articles/margashirsha-brahma-muhurta.jpg",
    "margashirsha-geeta-paath.jpg": "/data/user/0/ai.antigem/files/home/projects/Auto-Insta-Krishna/website/public/images/articles/margashirsha-geeta-paath.jpg",
    "margashirsha-tulsi-seva.jpg": "/data/user/0/ai.antigem/files/home/projects/Auto-Insta-Krishna/website/public/images/articles/margashirsha-tulsi-seva.jpg"
}

results = {}
for name, path in files_map.items():
    with open(path, 'rb') as f:
        file_bytes = f.read()
    
    # Upload to Catbox
    headers = {"User-Agent": "Mozilla/5.0"}
    files = {"fileToUpload": (name, file_bytes, "image/jpeg")}
    data = {"reqtype": "fileupload"}
    
    try:
        r = requests.post("https://catbox.moe/user/api.php", data=data, files=files, headers=headers, timeout=40)
        res_url = r.text.strip()
        if res_url.startswith("http"):
            results[name] = res_url
            print(f"Uploaded {name} -> {res_url}")
        else:
            print(f"Failed {name}: {res_url}")
    except Exception as e:
        print(f"Error {name}: {e}")

import json
with open('/data/user/0/ai.antigem/files/home/projects/AINews-KrishnaVibez/uploaded_catbox_article_images.json', 'w') as f:
    json.dump(results, f, indent=2)
print("Finished!")
