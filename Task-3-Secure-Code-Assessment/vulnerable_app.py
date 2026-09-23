import sqlite3
import hashlib

DATABASE = "vulnerable_users.db"


def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    conn.commit()
    conn.close()


def register_user():
    print("\n--- Register ---")

    username = input("Username: ")
    password = input("Password: ")

    # VULNERABILITY:
    # Fast SHA-256 is not ideal for password storage.
    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        # VULNERABILITY:
        # User input is directly inserted into SQL.
        query = f"""
            INSERT INTO users (username, password, role)
            VALUES ('{username}', '{password_hash}', 'user')
        """

        cursor.execute(query)

        conn.commit()

        print("User registered.")

    except sqlite3.Error as error:
        print("Database error:", error)

    finally:
        conn.close()


def login_user():
    print("\n--- Login ---")

    username = input("Username: ")
    password = input("Password: ")

    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # VULNERABILITY:
    # SQL injection due to string interpolation.
    query = f"""
        SELECT id, username, role
        FROM users
        WHERE username = '{username}'
        AND password = '{password_hash}'
    """

    try:
        cursor.execute(query)

        user = cursor.fetchone()

        if user:
            print("\nLogin successful!")
            print("ID:", user[0])
            print("Username:", user[1])
            print("Role:", user[2])
        else:
            print("Invalid username or password.")

    except sqlite3.Error as error:
        print("Database error:", error)

    finally:
        conn.close()


def view_users():
    print("\n--- Users ---")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, role FROM users"
    )

    users = cursor.fetchall()

    for user in users:
        print(
            f"ID: {user[0]} | "
            f"Username: {user[1]} | "
            f"Role: {user[2]}"
        )

    conn.close()


def main():
    create_database()

    while True:
        print("\n================================")
        print("     VULNERABLE USER SYSTEM")
        print("================================")
        print("1. Register")
        print("2. Login")
        print("3. View Users")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

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
            print("Invalid choice.")


if __name__ == "__main__":
    main()