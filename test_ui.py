from playwright.sync_api import sync_playwright
import os

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        file_path = f"file:///{os.path.abspath('templates/index.html')}"
        page.goto(file_path)
        
        print("Page loaded.")
        
        # Click the fast load button
        try:
            page.click("text=Tốt 1: Khang Thịnh", timeout=2000)
            print("Clicked Khang Thinh")
            page.wait_for_timeout(1000)
            
            # Click assessment
            page.click("text=CHẠY THẨM ĐỊNH AI 360", timeout=2000)
            print("Clicked Assessment")
            page.wait_for_timeout(1000)
            
            # Click cross sell
            page.click("text=TÌM KIẾM CƠ HỘI CROSS SELL", timeout=2000)
            print("Clicked Cross Sell")
            page.wait_for_timeout(2000)
            
            print("All clicks successful without fatal crash.")
        except Exception as e:
            print(f"Error during click: {e}")
        
        browser.close()

test()
