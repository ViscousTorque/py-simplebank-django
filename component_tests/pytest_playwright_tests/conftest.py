from typing import AsyncGenerator
from playwright.async_api import async_playwright, Browser, Page
import pytest_asyncio


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
