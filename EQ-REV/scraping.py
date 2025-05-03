import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import shutil
import os


zepto_url = "https://www.zeptonow.com/brand/Lay's/18d6cb72-65aa-4881-8984-a08aa295dd35?pvid=351db1e6-d693-4a28-88a8-2d59e864f67a"

def setup_driver():
    # Create a unique temporary directory for Chrome profile
    temp_profile_dir = tempfile.mkdtemp()

    chrome_options = Options()
  
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(f"--user-data-dir={temp_profile_dir}")

    try:
        service = Service()  # add executable_path="path/to/chromedriver" if needed
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver, temp_profile_dir
    except WebDriverException as e:
        print(f"Error setting up WebDriver: {e}")
        # Clean up temp directory
        shutil.rmtree(temp_profile_dir)
        return None, None

def test_zepto_connection():
    driver, temp_profile_dir = setup_driver()
    if not driver:
        return

    try:
        print("Navigating to Zepto URL...")
        driver.get(zepto_url)
        time.sleep(3)  # Wait for content to load

        print("Page Title:", driver.title)
        if "Zepto" in driver.title:
            print("✅ Successfully loaded the Zepto page.")
        else:
            print("⚠️ Page loaded, but title is unexpected.")

    except Exception as e:
        print(f"❌ Error during navigation: {e}")
    finally:
        driver.quit()
        shutil.rmtree(temp_profile_dir)  


test_zepto_connection()
