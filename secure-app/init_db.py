import sqlite3
from database import DB_FILE

def initialize_database():
    """Creates the necessary tables if they don't exist."""
    print(f"Initializing database at: {DB_FILE}")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            owner_username TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            comment_text TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialization complete.")

if __name__ == '__main__':
    # This allows you to still run it manually if you ever need to
    initialize_database()