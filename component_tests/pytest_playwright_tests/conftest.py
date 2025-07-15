from typing import AsyncGenerator
from playwright.async_api import async_playwright, Browser, Page
import pytest
import pytest_asyncio
from .utils.db import seed_users, clear_users
from .utils.test_factories import generate_fake_users

@pytest.fixture(scope="session", autouse=True)
def seed_test_users():
    known_users = [
        {
            "username": "viscous",
            "password": "viscousSecret",
            "full_name": "ViscousTorque",
            "email": "vistorq@example.com",
            "role": "depositor",
            "is_verified": False,
        },
    ]
    fake_users = generate_fake_users(2)
    all_users = known_users + fake_users

    seed_users(all_users)
    yield
    clear_users()

# if you make this session scope, the test hangs at test_page newcontext()
@pytest_asyncio.fixture
async def browser_session() -> AsyncGenerator[Browser, None]:
    async with async_playwright() as p:
        # use non-headless to debug
        # browser = await p.chromium.launch(headless=False, slow_mo=500)
        browser = await p.chromium.launch(headless=True, slow_mo=500)
        yield browser
        await browser.close()


@pytest_asyncio.fixture
async def test_page(browser_session: Browser) -> AsyncGenerator[Page, None]:
    context = await browser_session.new_context()
    page = await context.new_page()
    yield page
    await context.close()
