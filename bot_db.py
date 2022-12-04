import sqlite3

conn = sqlite3.connect('sqlite3.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS event_list(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_event TEXT NOT NULL,
    manager TEXT NOT NULL,
    manager_email TEXT NOT NULL,
    user_count INT NOT NULL, 
    date_register TEXT);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS event(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    surname TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL);
""")

conn.commit()

