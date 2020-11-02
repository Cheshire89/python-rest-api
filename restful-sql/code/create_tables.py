import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table_query = "CREATE TABLE IF NOT EXISTS users (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, username text NOT NULL UNIQUE, password text)"
cursor.execute(create_table_query)

create_table_query = "CREATE TABLE IF NOT EXISTS items (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, name text, price real)"
cursor.execute(create_table_query)


connection.commit()
connection.close()
