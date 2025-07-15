import pytest
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
