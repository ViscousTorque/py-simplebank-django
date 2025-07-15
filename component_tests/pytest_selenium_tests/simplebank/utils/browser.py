import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():
    selenium_url = os.getenv("SELENIUM_REMOTE_URL", "http://localhost:4444/wd/hub")

    options = Options()
    options.add_argument("--headless")  # not strictly needed for remote
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return webdriver.Remote(
        command_executor=selenium_url,
        options=options
    )
