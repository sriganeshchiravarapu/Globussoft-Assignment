import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# ── Headers to mimic a real browser ──────────────────────────────────────────
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
}

BASE_URL = "https://www.amazon.in/s?k=laptops&page={page}"

def get_page(page_num):
    url = BASE_URL.format(page=page_num)
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print(f"  ⚠️  Page {page_num} returned status {response.status_code}")
            return None
    except Exception as e:
        print(f"  ❌ Error fetching page {page_num}: {e}")
        return None

def parse_products(soup):
    products = []

    # All product cards on the page
    items = soup.find_all("div", {"data-component-type": "s-search-result"})
    print(f"  Found {len(items)} items on this page")

    for item in items:
        # ── Ad or Organic ────────────────────────────────────────────────────
        sponsored_tag = item.find("span", string=lambda t: t and "Sponsored" in t)
        result_type = "Ad" if sponsored_tag else "Organic"

        # ── Title ────────────────────────────────────────────────────────────
        title_tag = item.find("h2")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # ── Price ────────────────────────────────────────────────────────────
        price_tag = item.find("span", class_="a-price-whole")
        price = price_tag.get_text(strip=True).replace(",", "") if price_tag else "N/A"
        if price != "N/A":
            price = "₹" + price

        # ── Rating ───────────────────────────────────────────────────────────
        rating_tag = item.find("span", class_="a-icon-alt")
        rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

        # ── Image URL ────────────────────────────────────────────────────────
        img_tag = item.find("img", class_="s-image")
        image_url = img_tag["src"] if img_tag else "N/A"

        # ── Product URL ──────────────────────────────────────────────────────
        link_tag = item.find("a", class_="a-link-normal", href=True)
        product_url = ("https://www.amazon.in" + link_tag["href"]) if link_tag else "N/A"

        products.append({
            "Title":       title,
            "Price":       price,
            "Rating":      rating,
            "Image URL":   image_url,
            "Result Type": result_type,
            "Product URL": product_url,
        })

    return products

def main():
    all_products = []
    total_pages = 5  # Scrape 5 pages (~60–80 products)

    print("🚀 Starting Amazon laptop scraper...\n")

    for page in range(1, total_pages + 1):
        print(f"📄 Scraping page {page}/{total_pages}...")
        soup = get_page(page)

        if soup:
            products = parse_products(soup)
            all_products.extend(products)
        else:
            print(f"  Skipping page {page}")

        time.sleep(2)  # polite delay between requests

    # ── Save to CSV with timestamp ────────────────────────────────────────────
    if all_products:
        df = pd.DataFrame(all_products)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"amazon_laptops_{timestamp}.csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")

        print(f"\n✅ Done! Scraped {len(all_products)} products.")
        print(f"📁 Saved to: {filename}")
        print(df.head())
    else:
        print("\n❌ No products found. Amazon may have blocked the request.")
        print("   Try again after a few minutes or change your User-Agent.")

if __name__ == "__main__":
    main()