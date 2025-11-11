import asyncio
from playwright.async_api import async_playwright
import re, os, time, requests

# === CONFIGURATION ===
URL = "https://shop.travisscott.com/"
STATE_FILE = "state.txt"
WEBHOOK_URL = ""
CHECK_INTERVAL = 300  # seconds = 5 minutes

# === HELPERS ===

def send_discord(message: str):
    """Send a message to Discord via webhook."""
    payload = {"content": message}
    try:
        r = requests.post(WEBHOOK_URL, json=payload)
        if r.status_code in (200, 204):
            print("✅ Discord notification sent.")
        else:
            print(f"⚠️ Discord error: {r.status_code} {r.text}")
    except Exception as e:
        print(f"❌ Failed to send Discord message: {e}")

def count_soon(text: str) -> int:
    """Count occurrences of the word 'Soon' in the rendered HTML."""
    return len(re.findall(r'\bSoon\b', text))

async def fetch_rendered_html(url: str) -> str:
    """Load page with JavaScript using Playwright headless Chromium."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        # wait 3 seconds to allow JS to render product list
        await page.wait_for_timeout(3000)
        html = await page.content()
        await browser.close()
        return html

async def check_drop():
    """Main logic: check for 'Soon' count change."""
    print("🌐 Loading site...")
    html = await fetch_rendered_html(URL)
    new_count = count_soon(html)
    print(f"🧩 Found {new_count} 'Soon' tags on rendered page.")

    old_count = None
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                old_count = int(f.read().strip())
        except ValueError:
            old_count = None

    if old_count is None:
        print("ℹ️ First run — saving state.")
    elif new_count < old_count:
        print("🔥 Drop detected! Sending Discord alert...")
        message = (
            f"🔥 **Travis Scott shop update detected!**\n"
            f"🔗 {URL}\n"
            f"Old count: {old_count} → New count: {new_count}\n"
            f"👟 Drop might be live!"
        )
        send_discord(message)
    else:
        print("🕐 No drop yet.")

    with open(STATE_FILE, "w") as f:
        f.write(str(new_count))

async def main():
    print("🚀 Travis Scott Drop Checker (Playwright + Discord) started...")
    while True:
        await check_drop()
        print(f"⏳ Waiting {CHECK_INTERVAL/60:.1f} minutes before next check...\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
