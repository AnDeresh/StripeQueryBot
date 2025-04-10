import json
import os
import asyncio
from playwright.async_api import async_playwright

BASE_URL = "https://docs.stripe.com/api"

# Отримуємо базовий каталог проєкту (виходячи з того, що цей скрипт знаходиться в папці "scripts/")
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "stripe_urls.json")


async def get_links_with_eval():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Відкриває браузер для візуалізації
        page = await browser.new_page()

        await page.goto(BASE_URL, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)

        # JavaScript для витягування посилань із бокового меню
        hrefs = await page.evaluate("""
            () => {
                const anchors = Array.from(document.querySelectorAll("a"));
                const urls = anchors
                  .map(a => a.getAttribute("href"))
                  .filter(href => href && href.startsWith("/api/"))
                  .map(href => href.split("#")[0]);
                return Array.from(new Set(urls));
            }
        """)

        await browser.close()
        return sorted(hrefs)


async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Collecting all Stripe API doc URLs...")

    urls = await get_links_with_eval()
    print(f"Found {len(urls)} pages.")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(urls, f, indent=2)

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
    