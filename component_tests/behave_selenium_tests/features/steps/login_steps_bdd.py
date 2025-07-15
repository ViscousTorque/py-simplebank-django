from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from component_tests.behave_selenium_tests.pages.login_page import LoginPage


@given("I open the login page")
def step_open_login_page(context):
    context.page = LoginPage(context.driver)
    context.page.open()


@when('I enter "{username}" in the username field')
def step_enter_username(context, username):
    context.page.enter_username(username)


@when('I enter "{password}" in the password field')
def step_enter_password(context, password):
    context.page.enter_password(password)


@when('I click the "Login" button')
def step_click_login(context):
    context.page.click_login()


@then('I should see "{expected_name}" in the user profile')
def step_check_profile_name(context, expected_name):
    assert context.page.verify_user_profile(expected_name)


@then('I should see the error message "{error_message}"')
def step_check_error_message(context, error_message):
    toast_message = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "p-toast-message-error"))
    )
    error_detail = toast_message.find_element(By.CLASS_NAME, "p-toast-detail").text
    assert error_message in error_detail, (
        f"Expected '{error_message}', but got '{error_detail}'"
    )
    print(f"Verified toast error message: {error_detail}")

    WebDriverWait(context.driver, 5).until(EC.staleness_of(toast_message))
