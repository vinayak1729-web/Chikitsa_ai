import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table for users
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Create a table for user data
c.execute('''
CREATE TABLE IF NOT EXISTS user_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT,
    age INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

conn.commit()
conn.close()

print("Database and tables initialized successfully.")
