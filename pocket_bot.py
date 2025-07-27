import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from telegram_bot import is_running
from strategy import default_strategy
from datetime import datetime

load_dotenv()
EMAIL = os.getenv("PO_EMAIL")
PASSWORD = os.getenv("PO_PASSWORD")

price_history = {}
OTC_ASSETS = ["EURUSD_OTC", "GBPUSD_OTC", "USDJPY_OTC", "USDCHF_OTC", "AUDUSD_OTC"]

def run_bot():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://pocketoption.com/en/login/")
    time.sleep(5)
    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(10)

    for asset in OTC_ASSETS:
        price_history[asset] = []

    while True:
        if not is_running["status"]:
            time.sleep(5)
            continue

        for asset in OTC_ASSETS:
            try:
                switch_asset(driver, asset)
                time.sleep(2)
                price = get_otc_price(driver)
                if price:
                    price_history[asset].append(price)
                    if len(price_history[asset]) > 100:
                        price_history[asset].pop(0)

                    df = pd.DataFrame(price_history[asset], columns=["close"])
                    signal = default_strategy(df)
                    if signal:
                        place_trade(driver, signal)
                        log_signal(asset, signal, price)
                        capture_screenshot(driver, asset)
            except Exception as e:
                print(f"[{asset}] Error:", e)

        time.sleep(10)

def switch_asset(driver, asset_name):
    print(f"Switching to {asset_name}")
    # Simulate switch — actual implementation needed per UI

def get_otc_price(driver):
    try:
        price_element = driver.find_element(By.CSS_SELECTOR, ".price-value")
        return float(price_element.text.replace(',', '').strip())
    except:
        return None

def place_trade(driver, signal):
    try:
        action = ActionChains(driver)
        if signal == "BUY":
            btn = driver.find_element(By.CLASS_NAME, "btn-call")
        elif signal == "SELL":
            btn = driver.find_element(By.CLASS_NAME, "btn-put")
        else:
            return
        action.move_to_element(btn).click().perform()
        print(f"Trade executed: {signal}")
    except Exception as e:
        print("Trade click failed:", e)

def log_signal(asset, signal, price):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs("logs", exist_ok=True)
    with open("logs/trade_log.csv", "a") as f:
        f.write(f"{now},{asset},{signal},{price}\n")

def capture_screenshot(driver, asset):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("screenshots", exist_ok=True)
    filename = f"screenshots/{asset}_{timestamp}.png"
    driver.save_screenshot(filename)
