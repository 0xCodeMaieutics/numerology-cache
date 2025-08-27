from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from bs4 import BeautifulSoup

def get_dob_selenium(query_url):
    driver = None
    try:
        chrome_options = Options()
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        chrome_options.add_argument("--headless")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        driver.get(query_url)
        
        time.sleep(3)
        
        page_source = driver.page_source.lower()
        if "captcha" in page_source or "unusual traffic" in page_source:
            print("1. Running the script less frequently")
            print("2. Using a VPN")
            print("3. Running with --headless=false to solve CAPTCHA manually")
            return None
        
        wait = WebDriverWait(driver, 10)
        
        try:
            dob_element = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "wvKXQ"))
            )
            dob_text = dob_element.text.strip()
            
            g_img_element = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "zLZN1d"))
            )
            g_img_child_img = g_img_element.find_element(By.TAG_NAME, "img")
            img_src = g_img_child_img.get_attribute("src")
            print(img_src)

            if dob_text and img_src:
                return dob_text, img_src
        except TimeoutException:
            print("⏰ Timeout waiting for wvKXQ class element")
        
        # soup = BeautifulSoup(driver.page_source, 'html.parser')
        # dob_div = soup.find("div", class_="wvKXQ")
        
        # if dob_div:
        #     dob_text = dob_div.text.strip()
        #     if dob_text:
        #         print(f"✅ Found date of birth using BeautifulSoup: {dob_text}")
        #         return dob_text
        
        # Method 3: Try alternative class names that might contain birth info
        # alternative_classes = ["Z0LcW", "kno-rdesc", "Ap5OSd", "VuuXrf"]
        
        # for class_name in alternative_classes:
        #     try:
        #         elements = driver.find_elements(By.CLASS_NAME, class_name)
        #         for element in elements:
        #             text = element.text.strip()
        #             # Look for date patterns in the text
        #             if any(word in text.lower() for word in ['born', 'birth', 'december', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november']):
        #                 if any(char.isdigit() for char in text):  # Contains numbers (likely a date)
        #                     print(f"✅ Found potential birth info in {class_name}: {text}")
        #                     return text
        #     except NoSuchElementException:
        #         continue
        
        # Method 4: Look for any div containing birth-related keywords
        # all_divs = soup.find_all("div")
        # for div in all_divs:
        #     text = div.get_text().strip()
        #     if text and len(text) < 100:  # Reasonable length for a birth date
        #         text_lower = text.lower()
        #         if any(keyword in text_lower for keyword in ['born', 'birth']) and any(char.isdigit() for char in text):
        #             print(f"✅ Found birth info in generic div: {text}")
        #             return text
        
        print("❌ No date of birth information found")
        return None, None
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return None, None

    finally:
        # Always close the browser
        if driver:
            driver.quit()


scrape_url = "https://www.google.com/search?q=andrew+tate+date+of+birth"

if __name__ == "__main__":
    try:
        dob, img_src = get_dob_selenium(scrape_url)

        if dob and img_src:
            import json
            with open("dob_result.json", "w") as f:
                json.dump({"date_of_birth": {
                    "dob": dob, "src": img_src}}, f)
        else:
            print(f"\n💔 FAILED: Could not find date of birth")
            
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        if "chromedriver" in str(e).lower():
            print("\n🔧 ChromeDriver Issue Detected!")
        elif "timeout" in str(e).lower():
            print("\n⏰ Timeout Issue: Page took too long to load")
            print("Try increasing the wait times or checking your internet connection")