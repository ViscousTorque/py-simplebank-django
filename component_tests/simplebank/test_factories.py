from faker import Faker
from datetime import datetime, timezone

faker = Faker()

def generate_fake_user(**overrides):
    now = datetime.now(timezone.utc)

    return {
        "username": faker.user_name(),
        "password": faker.password(length=10), 
        "full_name": faker.name(), 
        "email": faker.unique.email(),
        "role": "depositor", 
        "is_verified": True,
        "password_changed_at": datetime(1, 1, 1, tzinfo=timezone.utc),
        "created_at": now, 
        **overrides
    }

def generate_fake_users(n=5):
    return [generate_fake_user() for _ in range(n)]
