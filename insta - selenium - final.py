import urllib.parse
import os
import json
from bs4 import BeautifulSoup
from seleniumbase import Driver
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import pandas as pd
import random
from pathlib import Path
import undetected_chromedriver as uc
import pickle

##############
def download_images(urls, folder="downloaded_pics"):
    os.makedirs(folder, exist_ok=True)  # Create folder if it doesn't exist

    for i, url in enumerate(urls):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                file_path = os.path.join(folder, f"image_{i}.jpg")
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Downloaded: {file_path}")
            else:
                print(f"Failed: {url}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")


def extract_image_urls(data):
    urls = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key == "candidates" and isinstance(value, list):
                urls.extend([img.get("url") for img in value if "url" in img])
            else:
                urls.extend(extract_image_urls(value))

    elif isinstance(data, list):
        for item in data:
            urls.extend(extract_image_urls(item))

    return urls

##############

directory = Path("downloaded_files")
driver_path = ChromeDriverManager().install()
if not directory.is_dir():
    driver_creation = Driver(uc=True, guest_mode=True, disable_cookies=True, headless=True)
else:
    pass






# Function to set up Selenium WebDriver with stealth mode
chrome_options = uc.ChromeOptions()
#chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--enable-webgl")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass detection
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

user_agents = [
    # Chrome (Windows, Mac, Linux)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

    # Firefox (Windows, Mac, Linux)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",

    # Edge (Windows, Mac)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",

    # Safari (Mac, iPhone, iPad)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.1 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/537.36",

    # Mobile Chrome & Firefox
    "Mozilla/5.0 (Linux; Android 14; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 6) Gecko/115.0 Firefox/115.0",
]

random_user_agent = random.choice(user_agents)
#chrome_options.add_argument(f"--user-agent={random_user_agent}")

driver = uc.Chrome(driver_executable_path=driver_path, options=chrome_options)





# If you want to remove the newline characters from each line, use a list comprehension
# done_data_ls = [line.strip() for line in data_2]


'''
https://www.instagram.com/stories/natgeo/
https://www.instagram.com/stories/sports_gallery01/3583753311409488862/
'''

url = "https://www.instagram.com/stories/natgeo/"
driver.get(url)
driver.maximize_window()
time.sleep(2)
# Load saved cookies
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
time.sleep(3)
driver.refresh()


try:
    # Wait until the ViewStory btn present
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[text()='View story']"))
    )
    # Check if the button is displayed
    if button.is_displayed():
        # Click the button
        button.click()
        print("Myday shown successfully.")
    else:
        print("Button is not visible.")
except Exception as e:
    print(f"An error occurred: {e}")




burp0_url = url
burp0_cookies = {"csrftoken": "PNMfxlURgcvsj0vZ3wcBar", "datr": "nWqxZzYYoi7X-_I4JpqPvuRu", "ig_did": "07FF5ECB-216D-4A96-9E3F-32F5B49B2DE2", "mid": "Z7FqnQALAAFtBcx2gjGWDu7uAIR8", "ig_nrcb": "1", "ds_user_id": "57049808672", "dpr": "1", "sessionid": "57049808672%3A4d4cMjOqHq2LdN%3A10%3AAYfDw9dKCoDFN4l19irCQdFMWQSBru5mkJ--CX7_jg", "wd": "1729x408", "rur": "\"CCO\\05457049808672\\0541773656904:01f73a76122455818d272aed4880a9ead0c1bd949746cd28245af064954a91b4ee4265c8\""}
burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Dpr": "2", "Viewport-Width": "1729", "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"macOS\"", "Sec-Ch-Ua-Platform-Version": "\"\"", "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Full-Version-List": "", "Sec-Ch-Prefers-Color-Scheme": "light", "Accept-Language": "en-US", "Accept-Encoding": "gzip, deflate", "Priority": "u=0, i"}
response = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
data = response.text
if response.status_code == 200:
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <script> tag with type="application/json"
    script_tag = soup.find_all('script', {'type': 'application/json'})

    if script_tag:
        image_urls = []

        for script in script_tag:
            try:
                data = json.loads(script.string)
                image_urls.extend(extract_image_urls(data))  # Reuse the previous function
            except (json.JSONDecodeError, TypeError):
                continue  # Skip if JSON is invalid

        print(len(image_urls))
image_urls_final  = [image_urls[i] for i in range(len(image_urls)) if i % 2 == 0]
download_images(image_urls_final)
