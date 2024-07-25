import requests
import os
import time
import re
import argparse
from urllib.parse import urljoin, urlparse
from collections import deque
import concurrent.futures
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "X-With-Links-Summary": "true"
}

MAX_WORKERS = 5  # Adjust this based on your needs and API rate limits
RATE_LIMIT = 1  # seconds between requests

def is_allowed_url(url, allowed_domains):
    parsed_url = urlparse(url)
    return any(domain in parsed_url.netloc for domain in allowed_domains)

def fetch_content(url):
    response = requests.get(f"{BASE_URL}{url}", headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch content from {url}: HTTP {response.status_code}")
        return None
    return response.text

def save_content(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def extract_title(markdown):
    match = re.search(r'Title: (.+)', markdown)
    return match.group(1).strip() if match else "Untitled"

def extract_links_section(markdown):
    match = re.search(r'Links/Buttons:\s*(.+?)(\n\n|\Z)', markdown, re.DOTALL)
    return match.group(1) if match else ""

def extract_links(links_section):
    link_pattern = re.compile(r'\[([^\]]+)\]\((https?://[^\)]+)\)')
    return link_pattern.findall(links_section)

def sanitize_filename(name):
    return re.sub(r'[^\w\-_\. ]', '_', name)

def process_url(url, output_dir, allowed_domains, multi_page):
    if url in processed_urls:
        return []

    print(f"Processing: {url}")
    
    content = fetch_content(url)
    if content is None:
        return []

    processed_urls.add(url)

    title = extract_title(content)
    sanitized_title = sanitize_filename(title)
    filename = os.path.join(output_dir, f"{sanitized_title}.md")
    
    if not os.path.exists(filename):
        save_content(content, filename)
        print(f"Saved: {filename}")

    if not multi_page:
        return []

    links_section = extract_links_section(content)
    links = extract_links(links_section)

    new_urls = []
    for link_text, link_url in links:
        absolute_url = urljoin(url, link_url)
        if is_allowed_url(absolute_url, allowed_domains) and absolute_url not in processed_urls:
            new_urls.append(absolute_url)

    return new_urls

def main(initial_url, output_dir, allowed_domains, multi_page):
    global processed_urls
    processed_urls = set()
    url_queue = deque([initial_url])

    os.makedirs(output_dir, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {}
        while url_queue or future_to_url:
            while url_queue and len(future_to_url) < MAX_WORKERS:
                url = url_queue.popleft()
                future = executor.submit(process_url, url, output_dir, allowed_domains, multi_page)
                future_to_url[future] = url

            if not future_to_url:
                break

            done, _ = concurrent.futures.wait(
                future_to_url, 
                timeout=RATE_LIMIT,
                return_when=concurrent.futures.FIRST_COMPLETED
            )

            for future in done:
                url = future_to_url[future]
                try:
                    new_urls = future.result()
                    url_queue.extend(new_urls)
                except Exception as e:
                    print(f"Failed to process {url}: {e}")
                del future_to_url[future]

            if not multi_page:
                break

            time.sleep(RATE_LIMIT)

    print(f"Scraping completed. Processed {len(processed_urls)} pages.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web scraper using Jina AI Reader API")
    parser.add_argument("url", help="Initial URL to scrape")
    parser.add_argument("output_dir", help="Directory to save scraped content")
    parser.add_argument("--allowed_domains", nargs='+', help="List of allowed domains to scrape", default=[])
    parser.add_argument("--multi_page", action="store_true", help="Enable multi-page scraping")
    
    args = parser.parse_args()

    if not args.allowed_domains:
        args.allowed_domains = [urlparse(args.url).netloc]

    main(args.url, args.output_dir, args.allowed_domains, args.multi_page)
