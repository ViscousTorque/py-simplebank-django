import asyncio
import re
import os
from playwright.async_api import Playwright, async_playwright, expect

APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:3000") # modified to work in docker compose

async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=True) # set True for CI
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(f"{APP_BASE_URL}/") # modified to work in docker compose
    await asyncio.sleep(0.2) # modified to work in docker compose, why do I need this?
    await expect(page.get_by_role("heading", name="Welcome to Simple Bank!")).to_be_visible()
    await expect(page.get_by_role("heading")).to_contain_text("Welcome to Simple Bank!")
    await page.get_by_role("heading", name="Welcome to Simple Bank!").click()
    await expect(page.locator("div").filter(has_text=re.compile(r"^Username$")).locator("i")).to_be_visible()
    await page.get_by_role("textbox", name="Username").click()
    await page.get_by_role("textbox", name="Username").fill("viscous")
    await expect(page.locator("div").filter(has_text=re.compile(r"^Password$")).locator("i")).to_be_visible()
    await page.get_by_role("textbox", name="Password").click()
    await page.get_by_role("textbox", name="Password").fill("viscousSecret")
    await expect(page.get_by_role("button", name="Login")).to_be_visible()
    await page.get_by_role("button", name="Login").click()
    await expect(page.get_by_text("User Profile")).to_be_visible()
    await expect(page.get_by_role("link", name="vistorq@example.com")).to_be_visible()
    await expect(page.locator("#app")).to_be_visible()
    await expect(page.get_by_role("link")).to_contain_text("vistorq@example.com")
    await expect(page.get_by_role("main")).to_contain_text("User Profile")
    await expect(page.get_by_role("button", name="Logout")).to_be_visible()
    await expect(page.get_by_label("Logout")).to_contain_text("Logout")
    await expect(page.get_by_role("heading")).to_contain_text("Welcome to Simple Bank!")
    await page.get_by_role("button", name="Logout").click()
    await page.close()

    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
