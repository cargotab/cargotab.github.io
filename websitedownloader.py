import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path

BASE_URL = "https://tanzilahmed.calicotab.com/ludc25/"
OUTPUT_DIR = "ybf-2022"
VISITED = set()

def make_relative_link(current_folder, target_path):
    """Return relative path from current folder to target_path/index.html"""
    current = Path(current_folder)
    target = Path(target_path) / "index.html"
    return os.path.relpath(target, start=current)

def save_html(url, folder_path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[x] Failed to download {url}: {e}")
        return

    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, "index.html")
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup.find_all("a", href=True):
        href = tag["href"]

        # Normalize
        if href.startswith(BASE_URL):
            href = href.replace(BASE_URL, "")
        elif href.startswith("/ybf-2022/"):
            href = href.replace("/ybf-2022/", "")

        if href.startswith("http") or href.startswith("#") or href.startswith("mailto:"):
            continue

        href = href.strip("/")
        if href:
            relative = make_relative_link(folder_path, os.path.join(OUTPUT_DIR, href))
            tag["href"] = relative
        else:
            tag["href"] = "index.html"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"[+] Saved: {file_path}")

def crawl(url):
    if url in VISITED or not url.startswith(BASE_URL):
        return
    VISITED.add(url)

    print(f"[*] Crawling: {url}")

    rel_path = url.replace(BASE_URL, "").rstrip("/")
    folder_path = os.path.join(OUTPUT_DIR, rel_path)
    save_html(url, folder_path)

    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
    except Exception:
        return

    for link in soup.find_all("a", href=True):
        next_url = urljoin(url, link["href"])
        if next_url.startswith(BASE_URL):
            crawl(next_url)

if __name__ == "__main__":
    crawl(BASE_URL)
    print("\n✅ Done! Local navigation paths now stay correct across folders.")
