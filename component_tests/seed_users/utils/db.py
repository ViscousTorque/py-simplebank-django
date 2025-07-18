import os
from datetime import datetime, timezone
import logging
import time

import psycopg2
from psycopg2.extras import execute_values, RealDictCursor

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_db_config():
    """
    This needs to be after import stage other POSTGRES_HOST is not found!
    """
    return {
        "dbname": os.getenv("POSTGRES_DB", "simple_bank_py"),
        "user": os.getenv("POSTGRES_USER", "admin"),
        "password": os.getenv("POSTGRES_PASSWORD", "adminSecret"),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
    }


SEEDED_USERNAMES = []


def get_connection(retries=5, delay=2):
    config = get_db_config()
    logger.debug(f"Trying to connect to DB with config: {config}")

    for attempt in range(1, retries + 1):
        try:
            conn = psycopg2.connect(**config)
            logger.debug("Successfully connected to DB.")
            return conn
        except psycopg2.OperationalError as e:
            logger.fatal(f"[{attempt}/{retries}] DB connection failed: {e}")
            time.sleep(delay)

    logger.error("All retries failed — could not connect to DB.")
    raise e


def seed_users(users):
    global SEEDED_USERNAMES
    values = []
    prepared_users = []
    logger.debug(f"Seeding {len(users)} user(s)...")

    # TODO: use Django make_password - need to django.setup() around here
    viscous_password_hash = "pbkdf2_sha256$870000$7YSTWLvu7itubaeyqtr1L1$vVTfmhlvGcoT8LUNruN1ekm6+m+2QjKyYy7Dya02GpA="

    for user in users:
        try:
            hashed_pw = viscous_password_hash
            entry = (
                user["username"],
                user.get("role", "depositor"),
                hashed_pw,
                user.get("full_name", user.get("full_name", "UNKNOWN")),
                user["email"],
                user.get("is_verified", False),
                user.get(
                    "password_changed_at", datetime(1970, 1, 1, tzinfo=timezone.utc)
                ),
                user.get("created_at", datetime.now(timezone.utc)),
            )
            values.append(entry)
            prepared_users.append(user["username"])
            logger.debug(f"Prepared for insert: {user['username']}")
        except Exception as e:
            logger.exception(
                f"Failed to prepare user {user.get('username', '[unknown]')}: {e}"
            )

    insert_query = """
        INSERT INTO users_user (
            username, role, hashed_password, full_name, email,
            is_verified, password_changed_at, created_at
        )
        VALUES %s
        ON CONFLICT (username) DO NOTHING;
    """

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                logger.debug("Attempting DB insert with the following values:")
                for val in values:
                    logger.debug(f" - {val[0]} | {val[3]} | {val[4]}")
                execute_values(cur, insert_query, values)
                conn.commit()
                logger.info(f"Successfully inserted users: {prepared_users}")
                SEEDED_USERNAMES.extend(prepared_users)
    except Exception as exc:
        logger.exception(f"Error {exc} inserting users into the database.")


def clear_users():
    if not SEEDED_USERNAMES:
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            # Delete from dependent table first
            cur.execute(
                """
                DELETE FROM authentication_session
                WHERE username_id IN (
                    SELECT id FROM users_user WHERE username = ANY(%s)
                );
            """,
                (SEEDED_USERNAMES,),
            )

            # Now delete the users
            cur.execute(
                "DELETE FROM users_user WHERE username = ANY(%s);", (SEEDED_USERNAMES,)
            )
            conn.commit()

    SEEDED_USERNAMES.clear()

def get_all_users():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users_user;")
            return cur.fetchall()
