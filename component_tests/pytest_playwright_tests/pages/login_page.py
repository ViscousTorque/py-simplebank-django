import os
import logging
from playwright.async_api import Page, expect, TimeoutError as PlaywrightTimeout

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

class LoginPage:
    def __init__(self, page: Page):
        logging.info("Constructing login page")
        self.page = page
        self.url = os.getenv("APP_BASE_URL", "http://localhost:3000")
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("xpath=//button[.//span[text()='Login']]")

    async def open(self):
        logger.info(f"[OPEN] Navigating to {self.url}")
        await self.page.goto(self.url, timeout=15000)
        logger.info("[OPEN] Page loaded.")

    async def enter_username(self, username: str):
        await self.username_input.wait_for(state="visible", timeout=10000)
        await self.username_input.fill(username)

    async def enter_password(self, password: str):
        await self.password_input.wait_for(state="visible", timeout=10000)
        await self.password_input.fill(password)

    async def click_login(self):
        await self.login_button.wait_for(state="attached", timeout=10000)
        await self.login_button.click()

    async def verify_user_profile(self, expected_name: str) -> bool:
        logger.info(f"[VERIFY] Waiting for user profile with name: '{expected_name}'")
        locator = self.page.locator("div.p-card-content span.m-2", has_text=expected_name)

        try:
            await expect(locator).to_contain_text(expected_name, timeout=10000)
            return True
        except TimeoutError:
            logger.error("[ERROR] Timeout waiting for profile name to be visible")
            return False


    async def verify_error_message(self, error_message: str) -> bool:
        try:
            logger.info(f"[VERIFY] Waiting for toast with error message: '{error_message}'")
            error = self.page.locator("div.p-toast-message-error >> div.p-toast-detail", has_text=f"{error_message}")
            await error.wait_for(timeout=10000)
            logger.debug(f"[ACTUAL] Found error toast with message: '{error_message}'")
            return await error.is_visible()
        except PlaywrightTimeout:
            logger.error(f"[ERROR] Timeout waiting for error message: {error}")
            return False
