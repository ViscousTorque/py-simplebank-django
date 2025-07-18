import sys
from component_tests.seed_users.utils.db import seed_users, get_all_users
from component_tests.seed_users.utils.test_factories import generate_fake_users

def main():
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

    print(f"Seeding {len(all_users)} users...")
    seed_users(all_users)

    inserted_users = get_all_users()
    if len(inserted_users) >= len(all_users):
        print(f"✅ Successfully seeded {len(inserted_users)} users.")
        sys.exit(0)
    else:
        print(f"❌ User seeding failed. Only {len(inserted_users)} found in DB.")
        sys.exit(1)

if __name__ == "__main__":
    main()
