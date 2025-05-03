from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Setup Selenium WebDriver
options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options)

# Navigate to Zepto Lay's brand page
zepto_url = "https://www.zeptonow.com/brand/Lay's/18d6cb72-65aa-4881-8984-a08aa295dd35"
print("Navigating to Zepto URL...")
driver.get(zepto_url)


wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-testid='product-card']")))

# Scroll to load all products
SCROLL_PAUSE = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(3)

# Extract product info
product_cards = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='product-card']")
print(f"Found {len(product_cards)} products.")

data = []

for index, card in enumerate(product_cards, start=1):
    try:
        name = card.find_element(By.CSS_SELECTOR, "[data-testid='product-card-name']").text
        price_texts = card.find_elements(By.CSS_SELECTOR, "[data-testid='product-card-price']")
        pack_info = card.find_element(By.CSS_SELECTOR, "[data-testid='product-card-quantity']").text
        stock_status = "Out of Stock" if "Out of Stock" in card.text else "In Stock"

        mrp = discounted_price = ""
        if len(price_texts) == 1:
            mrp = discounted_price = price_texts[0].text
        elif len(price_texts) == 2:
            mrp = price_texts[0].text
            discounted_price = price_texts[1].text

        product_id = card.get_attribute("href")

        data.append({
            "Product Name": name,
            "Product ID": product_id,
            "Brand Name": "Lay's",
            "MRP": mrp,
            "Discounted Price": discounted_price,
            "Stock Status": stock_status,
            "Pack Info": pack_info,
            "Position": index
        })

    except Exception as e:
        print(f"❌ Error extracting product at position {index}: {e}")

# Save or print
df = pd.DataFrame(data)
df.to_csv(r"C:\Users\rajav\OneDrive\Desktop\zepto_lays_products.csv", index=False)
print("✅ Data saved to 'zepto_lays_products.csv'.")

driver.quit()
