from component_tests.behave_selenium_tests.utils.browser import get_driver
from component_tests.behave_selenium_tests.utils.db import seed_users, clear_users
from component_tests.behave_selenium_tests.utils.test_factories import generate_fake_users

def before_all(context):
    context.driver = get_driver()

    # Seed known and fake users
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
    context.test_users = all_users  # Optional: Access in step definitions

def after_all(context):
    context.driver.quit()
    clear_users()
