import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://awakening.wiki/"
START_PATH = "/"
visited = set()
pages = {}

def get_links_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for a in soup.select("a[href^='/']"):
        href = a['href'].split('#')[0]
        if href.startswith("/") and '.' not in href and href not in visited:
            links.append(href)
    return list(set(links))

def scrape_page(path):
    if path in visited or len(visited) >= 30:
        return
    visited.add(path)

    full_url = BASE_URL + path
    print(f"Scraping {full_url}")
    try:
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Error scraping {full_url}: {e}")
        return

    # Try to find page title
    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else path

    # Extract all visible content
    content_div = soup.find("main") or soup.body
    if not content_div:
        print(f"Skipping {full_url} (no content found)")
        return

    text_elements = content_div.find_all(["p", "li"])
    text = "\n".join(t.get_text(strip=True) for t in text_elements if t.get_text(strip=True))

    if text:
        pages[title] = text

    # Crawl linked internal pages
    for link in get_links_from_page(full_url):
        scrape_page(link)
        time.sleep(0.5)

# Run it
scrape_page(START_PATH)

# Save to file
with open("dune_wiki.txt", "w", encoding="utf-8") as f:
    for title, content in pages.items():
        f.write(f"# {title}\n{content}\n\n")

print(f"✅ Done. {len(pages)} pages saved to dune_wiki.txt")
