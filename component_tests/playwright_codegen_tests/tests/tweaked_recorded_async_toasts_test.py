"""
This code is just to show some examples of changes from the recorded test, here are 
some ideas where potential improvements could be made before the refactoring to POM:
i) observing greeting toasts alerts (although could lengthen overall test run)
ii) using the ui with observing the toasts
"""
import asyncio
import re
import os
from playwright.async_api import async_playwright, Page, expect, Playwright

async def expect_toast_then_disappear(page: Page, message: str, timeout: int = 10000):
    toast = page.get_by_role("alert").filter(has_text=message)
    await expect(toast).to_be_visible(timeout=timeout)
    await toast.wait_for(state="detached", timeout=timeout)

APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:3000") # modified to work in docker compose

async def run_tweaked_async_login_toasts(name: str, playwright: Playwright):
    print(f"    Running: {name}")
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(f"{APP_BASE_URL}/") 
    await asyncio.sleep(0.2)  # You can reduce this later if needed

    # Step 1: login page visible
    await expect(page.get_by_role("heading", name="Welcome to Simple Bank!")).to_be_visible()
    await expect(
        page.locator("div").filter(has_text=re.compile(r"^Username$")).locator("i")
    ).to_be_visible()
    await expect(page.get_by_role("button", name="Login")).to_be_visible()

    # Step 2: Fill in credentials and log in
    await page.get_by_role("textbox", name="Username").fill("viscous")
    await page.get_by_role("textbox", name="Password").fill("viscousSecret")
    await page.get_by_role("button", name="Login").click()

    # Step 3: Wait for login toast to appear and disappear
    await expect_toast_then_disappear(page, "Hello, ViscousTorque")

    # Step 4: Check profile data is visible
    await expect(page.locator('div.p-card-title[data-pc-section="title"]')).to_have_text("User Profile")
    await expect(page.locator('div.p-card-content >> text=ViscousTorque')).to_be_visible()
    await expect(page.locator('div.p-card-content >> text=vistorq@example.com')).to_be_visible()

    # Step 5: Logout and observe goodbye toast
    await expect(page.get_by_role("button", name="Logout")).to_be_visible()
    await page.get_by_role("button", name="Logout").click()
    await expect_toast_then_disappear(page, "Goodbye, ViscousTorque!")

    await page.close()
    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run_tweaked_async_login_toasts("Login toast test", playwright)


if __name__ == "__main__":
    asyncio.run(main())

