import pytest
import logging
from .pages.login_page import LoginPage

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
@pytest.mark.parametrize("username, password, full_name", [
    ("viscous", "viscousSecret", "ViscousTorque"),
])
async def test_successful_login(test_page, username, password, full_name):
    login = LoginPage(test_page)
    await login.open()
    await login.enter_username(username)
    await login.enter_password(password)
    await login.click_login()

    assert await login.verify_user_profile(full_name)


@pytest.mark.asyncio
@pytest.mark.parametrize("username, password, error_message", [
    ("viscous", "wrongpass", "Invalid username or password"),
    ("unknown", "whatever", "Invalid username or password"),
])
async def test_unsuccessful_login(test_page, username, password, error_message):
    login = LoginPage(test_page)
    await login.open()
    await login.enter_username(username)
    await login.enter_password(password)
    await login.click_login()

    assert await login.verify_error_message(error_message)
