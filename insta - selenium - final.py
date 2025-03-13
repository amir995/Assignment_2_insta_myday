import urllib.parse
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

url = "https://www.instagram.com/stories/sports_gallery01/3583753311409488862/"
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

time.sleep(100)

# Set up the directory to save downloaded files
directory = Path("downloaded_pics")
directory.mkdir(exist_ok=True)
'''
try:
    while True:
        wait = WebDriverWait(driver, 10)
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button']//svg[@aria-label='Next']")))
        next_button.click()
except Exception as E:
    print(E)

'''



'''
image_elements = driver.find_elements(By.XPATH, "//img[contains(@class, 'y-yJ5') or contains(@class, 'FFVAD')]")
# Download the image
if image_elements:
    image_url = image_elements[0].get_attribute("src")
    image_data = requests.get(image_url).content
    with open(directory / "instagram_story_image.jpg", "wb") as handler:
        handler.write(image_data)
    print("Image downloaded successfully.")
else:
    print("No image found in the story.")
time.sleep(1000)
'''