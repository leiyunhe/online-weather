import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE qw (qttime TEXT, city_name TEXT, weather TEXT, temperature TEXT)')
print("Table created successfully")
conn.close()