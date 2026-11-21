import shutil
import os
import requests
import json
import re

IMG_MAPPING = {
    "openai_o3": r"C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\openai_o3_editorial_v2_1795253253328.jpg",
    "silicon_datacenter": r"C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\silicon_datacenter_editorial_1795253231483.jpg",
    "humanoid_robot": r"C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\humanoid_robot_editorial_1795253233641.jpg"
}

dest_dir = r"e:\Paresh\Auto Post\AINews-KrishnaVibez\public\images"
os.makedirs(dest_dir, exist_ok=True)

uploaded_urls = {}

def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    with open(file_path, "rb") as f:
        data = {"reqtype": "fileupload"}
        files = {"fileToUpload": (os.path.basename(file_path), f, "image/jpeg")}
        resp = requests.post(url, data=data, files=files, timeout=30)
    if resp.status_code == 200 and resp.text.startswith("http"):
        return resp.text.strip()
    raise RuntimeError(f"Catbox upload failed: {resp.status_code} {resp.text}")

for key, src_path in IMG_MAPPING.items():
    dest_path = os.path.join(dest_dir, f"{key}.jpg")
    shutil.copy2(src_path, dest_path)
    print(f"Copied {key} -> {dest_path} ({os.path.getsize(dest_path)//1024} KB)")
    
    catbox_url = upload_to_catbox(dest_path)
    print(f"Uploaded {key} to Catbox: {catbox_url}")
    uploaded_urls[key] = catbox_url

# Save mapping
mapping_file = r"e:\Paresh\Auto Post\AINews-KrishnaVibez\editorial_catbox_urls.json"
with open(mapping_file, "w") as f:
    json.dump(uploaded_urls, f, indent=2)

print("\nSUCCESS! Uploaded URLs:")
print(json.dumps(uploaded_urls, indent=2))
