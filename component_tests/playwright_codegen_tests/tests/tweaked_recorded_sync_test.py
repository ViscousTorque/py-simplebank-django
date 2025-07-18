"""
This code is just to show some examples of changes from the recorded test, here are 
some ideas where potential improvements could be made before the refactoring to POM:
i) observing greeting toasts alerts (although could lengthen overall test run)
ii) using the ui with and without observing the toasts
"""
import re
import time
import os
from playwright.sync_api import Playwright, sync_playwright, expect


# tweak to observe toast appearing with text and disappearing
def expect_toast_then_disappear(page, message, timeout=10000):
    toast = page.get_by_role("alert").filter(has_text=message)
    expect(toast).to_be_visible(timeout=timeout)
    toast.wait_for(state="detached", timeout=timeout)

APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:3000") # modified to work in docker compose

def run_tweaked_sync_login_toasts(name, playwright: Playwright) -> None:
    print(f"    Running: {name}")
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto(f"{APP_BASE_URL}/")
    time.sleep(0.2)

    # step 1 - Observe the login page, using username and password, click Login
    expect(page.get_by_role("heading", name="Welcome to Simple Bank!")).to_be_visible()
    expect(page.locator("div").filter(has_text=re.compile(r"^Username$")).locator("i")).to_be_visible()
    expect(page.get_by_role("button", name="Login")).to_be_visible()

    # step 2 - login with username and password
    page.get_by_role("textbox", name="Username").fill("viscous")
    page.get_by_role("textbox", name="Password").fill("viscousSecret")
    page.get_by_role("button", name="Login").click()

    # step 3 - observe behaviour of hello toast
    expect_toast_then_disappear(page, "Hello, ViscousTorque")

    # step 4 - check user profile is visible with user details
    # Check that the profile card title is visible and correct
    expect(page.locator('div.p-card-title[data-pc-section="title"]')).to_have_text("User Profile")

    # Check that the user's name and email are visible in their exact locations
    expect(page.locator('div.p-card-content >> text=ViscousTorque')).to_be_visible()
    expect(page.locator('div.p-card-content >> text=vistorq@example.com')).to_be_visible()

    # step 5 - check that the Logout button is visible, click and observe behaviour of goodbye toast
    expect(page.get_by_role("button", name="Logout")).to_be_visible()
    page.get_by_role("button", name="Logout").click()
    expect_toast_then_disappear(page, "Goodbye, ViscousTorque!")
    page.close()

    # ---------------------
    context.close()
    browser.close()


def run_tweaked_sync_login(name, playwright: Playwright) -> None:
    print(f"    Running: {name}")
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://frontend/")

    # step 1 - Observe the login page, using username and password, click Login
    expect(page.get_by_role("heading", name="Welcome to Simple Bank!")).to_be_visible()
    expect(page.locator("div").filter(has_text=re.compile(r"^Username$")).locator("i")).to_be_visible()
    expect(page.get_by_role("button", name="Login")).to_be_visible()

    # step 2 - login with username and password
    page.get_by_role("textbox", name="Username").fill("viscous")
    page.get_by_role("textbox", name="Password").fill("viscousSecret")
    page.get_by_role("button", name="Login").click()

    # step 3 - check user profile is visible with user details
    # Check that the profile card title is visible and correct
    expect(page.locator('div.p-card-title[data-pc-section="title"]')).to_have_text("User Profile")

    # Check that the user's name and email are visible in their exact locations
    expect(page.locator('div.p-card-content >> text=ViscousTorque')).to_be_visible()
    expect(page.locator('div.p-card-content >> text=vistorq@example.com')).to_be_visible()

    # step 4 - check that the Logout button is visible, click
    expect(page.get_by_role("button", name="Logout")).to_be_visible()
    page.get_by_role("button", name="Logout").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run_tweaked_sync_login_toasts("run_tweaked_sync_login_toasts", playwright)
    run_tweaked_sync_login("run_tweaked_sync_login", playwright)


