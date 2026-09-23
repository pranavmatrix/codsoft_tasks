import sqlite3
import hashlib
import secrets
import hmac
import getpass

DATABASE = "secure_users.db"


def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )

    return password_hash.hex(), salt.hex()


def verify_password(password, stored_hash, stored_salt):
    salt = bytes.fromhex(stored_salt)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )

    return hmac.compare_digest(
        password_hash.hex(),
        stored_hash
    )


def register_user():
    print("\n--- Register User ---")

    username = input("Username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    if len(username) > 50:
        print("Username is too long.")
        return

    password = getpass.getpass("Password: ")

    if len(password) < 8:
        print("Password must contain at least 8 characters.")
        return

    confirm = getpass.getpass("Confirm password: ")

    if password != confirm:
        print("Passwords do not match.")
        return

    password_hash, salt = hash_password(password)

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (username, password_hash, salt, role)
            VALUES (?, ?, ?, ?)
            """,
            (username, password_hash, salt, "user")
        )

        conn.commit()
        conn.close()

        print("User registered successfully.")

    except sqlite3.IntegrityError:
        print("Username already exists.")

    except sqlite3.Error:
        print("Database error occurred.")


def login_user():
    print("\n--- Login ---")

    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, username, password_hash, salt, role
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        user = cursor.fetchone()
        conn.close()

        if user is None:
            print("Invalid username or password.")
            return

        user_id, stored_username, stored_hash, stored_salt, role = user

        if verify_password(password, stored_hash, stored_salt):
            print("\nLogin successful!")
            print("User ID :", user_id)
            print("Username:", stored_username)
            print("Role    :", role)
        else:
            print("Invalid username or password.")

    except sqlite3.Error:
        print("Database error occurred.")


def view_users():
    print("\n--- Registered Users ---")

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, username, role FROM users"
        )

        users = cursor.fetchall()
        conn.close()

        if not users:
            print("No users registered.")
            return

        for user in users:
            print(
                f"ID: {user[0]} | "
                f"Username: {user[1]} | "
                f"Role: {user[2]}"
            )

    except sqlite3.Error:
        print("Unable to read database.")


def main():
    create_database()

    while True:
        print("\n================================")
        print("      SECURE USER SYSTEM")
        print("================================")
        print("1. Register")
        print("2. Login")
        print("3. View Users")
        print("4. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            register_user()

        elif choice == "2":
            login_user()

        elif choice == "3":
            view_users()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()