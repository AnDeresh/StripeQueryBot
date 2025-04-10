import json
import os
import asyncio
from playwright.async_api import async_playwright
from tqdm.asyncio import tqdm

INPUT_PATH = "data/stripe_urls.json"
OUTPUT_PATH = "data/stripe_docs.json"
BASE_URL = "https://docs.stripe.com"

SELECTORS = [
    "main h1", "main h2", "main h3",
    "main p", "main pre", "main code",
    "main li"
]


async def scrape_page(page, url_path):
    full_url = f"{BASE_URL}{url_path}"
    await page.goto(full_url, wait_until="domcontentloaded")
    await page.wait_for_timeout(1500)

    content_blocks = []

    for selector in SELECTORS:
        elements = await page.locator(selector).all()
        for el in elements:
            text = await el.inner_text()
            if text.strip():
                content_blocks.append(text.strip())

    return {
        "url": full_url,
        "content": "\n".join(content_blocks)
    }


async def main():
    with open(INPUT_PATH, "r") as f:
        urls = json.load(f)

    os.makedirs("data", exist_ok=True)

    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for url in tqdm(urls, desc="Scraping pages"):
            try:
                data = await scrape_page(page, url)
                results.append(data)
            except Exception as e:
                print(f"[!] Failed to scrape {url}: {e}")

        await browser.close()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"[✓] Saved {len(results)} pages to {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
