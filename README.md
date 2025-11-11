# Travis Scott Drop Checker 👟

A Python automation script that monitors the [Travis Scott website](https://shop.travisscott.com) for new drops and sends Discord alerts when something appears.

---

## Features
- Uses **Playwright** to render dynamic web pages  
- Detects **“Soon”** tags and product updates automatically  
- Sends **Discord webhook notifications**  
- Waits and refreshes at set intervals (default: every 5 minutes)

---

## Tech Stack
-  **Python 3.14**
-  **Playwright**
-  **Discord Webhooks**

---

## Setup Instructions

1. **Clone the repo**
   cmd:
   git clone https://github.com/seanzlli/travis-drop-checker.git
   cd travis-drop-checker

2. **Install dependencies**
   cmd:
   pip install playwright
   playwright install

3. **Run the bot**
   python travis_drop_checker_playwright.py

EXAMPLE OUTPUT
🚀 Travis Scott Drop Checker started...
🧩 Found 1 'Soon' tag(s) on rendered page.
🕐 No drop yet.
⏳ Waiting 5.0 minutes before next check...

FUTURE IMRPOVEMENTS
Add multi-site support (Nike, SNKRS, etc.)
Web dashboard for live tracking
Configurable check intervals

Author
Sean Zhu Liong Li (SeanZLLi)