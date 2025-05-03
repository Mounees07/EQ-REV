from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

driver.get("https://www.zeptonow.com/brand/Lay's/18d6cb72-65aa-4881-8984-a08aa295dd35")

wait = WebDriverWait(driver, 20)

# Step 1: Handle PIN code entry if popup appears
try:
    pin_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='pincode']")))
    pin_input.send_keys("600001")  # Use a valid city pincode like Chennai
    submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Submit')]")))
    submit_btn.click()
    print("✅ Pincode submitted.")
    time.sleep(5)  # Wait for products to load
except Exception as e:
    print("⚠️ No pincode prompt detected or already set.")

# Step 2: Try to find product cards
time.sleep(5)  # Let JS render product cards
product_cards = driver.find_elements(By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(@class,'flex-col')]")
print(f"🔍 Found {len(product_cards)} products.")

if product_cards:
    df = pd.DataFrame([{"Product Name": "Test Product"}])
    df.to_excel("zepto_test.xlsx", index=False)
    print("✅ Excel file 'zepto_test.xlsx' created.")
else:
    print("❌ Still no products found. Double-check rendered HTML after PIN is set.")

driver.quit()
