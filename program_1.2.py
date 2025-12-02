# Title: create_cities_db.py

import sqlite3

conn = sqlite3.connect('cities.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Cities (CityID INTEGER PRIMARY KEY NOT NULL, CityName TEXT, Population TEXT)''')

cursor.execute('''INSERT INTO Cites (CityName, Population) VALUES ("Jordan", 6800)''')

conn.commit()

conn.close()