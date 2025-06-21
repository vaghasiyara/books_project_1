from playwright.sync_api import sync_playwright
import os
from datetime import datetime

class BookScraper:
    def __init__(self, url):
        self.url = url
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
    def scrape_chapter(self, take_screenshot=True):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(self.url)
            
            content = page.inner_text("#mw-content-text")
            
            screenshot_path = None
            if take_screenshot:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"{self.screenshot_dir}/chapter_{timestamp}.png"
                page.screenshot(path=screenshot_path)
            
            browser.close()
            
            return {
                "content": content,
                "screenshot_path": screenshot_path,
                "source_url": self.url
            }
