import sqlite3
conn = sqlite3.connect('acms.db')
print("Opened database successfully")
conn.execute('''CREATE TABLE Hotel
        (HotelID INTEGER PRIMARY KEY AUTOINCREMENT,
         HotelName TEXT    NOT NULL,
         HotelPhone TEXT,
         HotelMail TEXT NOT NULL UNIQUE,
         HotelPassword TEXT NOT NULL,
         HotelAddress TEXT NOT NULL);''')
print("Table created successfully");

print("Opened database successfully")
conn.execute('''CREATE TABLE Charity
        (CharityID INTEGER PRIMARY KEY AUTOINCREMENT,
         CharityName TEXT    NOT NULL,
         CharityPhone TEXT ,
         CharityMail TEXT  NOT NULL UNIQUE ,
         CharityPassword TEXT  NOT NULL,
         CharityAddress TEXT  NOT NULL);''')
print("Table created successfully");

conn.close()