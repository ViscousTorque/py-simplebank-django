import os
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoginPage:
    """Page Object Model for Login Page"""

    def __init__(self, driver):
        self.driver = driver
        self.url = os.getenv("APP_BASE_URL", "http://localhost:3000")

    def open(self):
        logger.info(f"🌍 Navigating to: {self.url}")
        self.driver.get(self.url)

    def enter_username(self, username):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys(username)

    def enter_password(self, password):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        ).send_keys(password)

    def click_login(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Login']]"))
        ).click()

    def verify_user_profile(self, expected_name):
        print(f"[DEBUG] Waiting for user profile with name: '{expected_name}'")
        print(self.driver.page_source[:1000])

        try:
            profile = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//*[contains(normalize-space(text()), '{expected_name}')]",
                    )
                )
            )
            return profile.is_displayed()
        except TimeoutException:
            print(f"[ERROR] Timeout waiting for profile with {expected_name} to appear")
            return False

    def verify_error_message(self, error_message):
        error = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//div[contains(text(), '{error_message}')]")
            )
        )
        return error.is_displayed()
