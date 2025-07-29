import os
import time
import requests
from appium import webdriver
from appium.options.android import UiAutomator2Options

def wait_for_appium(host, port, timeout=60):
    url = f"http://{host}:{port}/status"
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(url)
            if response.ok and response.json()["value"]["ready"]:
                print("Appium is ready.")
                return True
        except requests.RequestException:
            pass
        print("⏳ Waiting for Appium to be ready...")
        time.sleep(2)
    raise TimeoutError(f"Appium not ready after {timeout} seconds")

def test_login_page():
    appium_host = os.getenv("APPIUM_HOST", "android-emulator")
    appium_port = 4723

    # Wait for Appium to be ready before creating the driver
    wait_for_appium(appium_host, appium_port)

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "13.0"
    options.device_name = "Android Emulator"
    options.browser_name = "Chrome"
    options.automation_name = "UiAutomator2"

    # options.set_capability("chromeOptions", {
    # "args": [
    #     "--disable-dev-shm-usage",
    #     "--no-sandbox",
    #     "--disable-gpu",
    #     "--headless"
    # ]})


    options.set_capability("disableHiddenApiPolicyCheck", True)
    options.set_capability("ignoreHiddenApiPolicyError", True)
    options.set_capability("skipUnlock", True)
    options.set_capability("chromedriverAutodownload", False)
    options.set_capability("relaxedSecurityEnabled", False)
    options.set_capability("chromedriverExecutable", "/opt/chromedrivers/chromedriver")

    driver_url = f"http://{appium_host}:{appium_port}"
    print(f'{driver_url=}')

    driver = webdriver.Remote(driver_url, options=options)

    try:
        driver.get("http://frontend")
        time.sleep(2)
        assert "Simple Bank" in driver.title
    finally:
        driver.quit()


