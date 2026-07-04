"""
Keep-alive for Streamlit Community Cloud apps.
A plain HTTP request does NOT wake a sleeping app (200 + static shell only),
so we drive a real headless browser and click the wake button if present.
Add or remove URLs in the APPS list.
"""
import sys
from playwright.sync_api import sync_playwright

APPS = [
    "https://turboquant-vit.streamlit.app",
    "https://skin-cancer-detection-saurabh.streamlit.app",
]
WAKE_BUTTON = "Yes, get this app back up!"

def visit(page, url):
    print(f"Visiting {url}", flush=True)
    page.goto(url, wait_until="domcontentloaded", timeout=120_000)
    page.wait_for_timeout(5_000)
    btn = page.get_by_role("button", name=WAKE_BUTTON)
    if btn.count() > 0:
        print(f"  ASLEEP -> clicking wake button for {url}", flush=True)
        btn.first.click()
        page.wait_for_timeout(60_000)
        print(f"  WOKE {url}", flush=True)
    else:
        print(f"  OK (already awake) {url}", flush=True)

def main():
    failures = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_context().new_page()
        for url in APPS:
            try:
                visit(page, url)
            except Exception as e:
                failures += 1
                print(f"  ERROR on {url}: {e}", flush=True)
        browser.close()
    if failures == len(APPS):
        sys.exit(1)

if __name__ == "__main__":
    main()
