# pylint: disable=redefined-outer-name
from pathlib import Path
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from component_tests.simplebank.pages.login_page import LoginPage

feature_path = Path(__file__).parent.parent / "features" / "login.feature"


@pytest.fixture(scope="module")
def driver():
    """Setup Chrome WebDriver."""
    from component_tests.simplebank.utils.browser import get_driver # pylint: disable=import-outside-toplevel

    driver = get_driver()
    yield driver
    driver.quit()


@scenario(str(feature_path), "Successful login")
def test_successful_login():
    pass


@scenario(str(feature_path), "Unsuccessful login")
def test_unsuccessful_login():
    pass


@given("I open the login page")
def open_login_page(driver):
    page = LoginPage(driver)
    page.open()


@when(parsers.parse('I enter "{username}" in the username field'))
def enter_username(driver, username):
    page = LoginPage(driver)
    page.enter_username(username)


@when(parsers.parse('I enter "{password}" in the password field'))
def enter_password(driver, password):
    page = LoginPage(driver)
    page.enter_password(password)


@when('I click the "Login" button')
def click_login(driver):
    page = LoginPage(driver)
    page.click_login()


@then(parsers.parse('I should see "{expected_name}" in the user profile'))
def check_profile_name(driver, expected_name):
    page = LoginPage(driver)
    assert page.verify_user_profile(expected_name)


@then(parsers.parse('I should see the error message "{error_message}"'))
def check_error_message(driver, error_message):
    # Wait for the toast to appear
    toast_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "p-toast-message-error"))
    )

    error_detail = toast_message.find_element(By.CLASS_NAME, "p-toast-detail").text
    assert (
        error_message in error_detail
    ), f"xpected '{error_message}', but got '{error_detail}'"

    print(f"Verified toast error message: {error_detail}")

    WebDriverWait(driver, 5).until(EC.staleness_of(toast_message))
