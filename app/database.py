import sqlite3


conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE tasks (UID INTEGER PRIMARY kEY AUTOINCREMENT, NAME TEXT, TASK TEXT, PRIORITY TEXT, COMPLETED INTEGER)')


print("Table created successfully")
conn.close()
