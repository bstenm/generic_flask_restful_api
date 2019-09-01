import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS stores (id INTEGER PRIMARY KEY, name text, feature1 text)")
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)")

connection.close()
