import sqlite3
conn = sqlite3.connect('acms.db')
print("Opened database successfully")
conn.execute('''CREATE TABLE Hotel
        (HotelID INT PRIMARY KEY     NOT NULL,
         HotelName TEXT    NOT NULL,
         HotelPhone TEXT     NOT NULL,
         HotelMail TEXT,
         HotelPassword TEXT,
         HotelAddress TEXT);''')
print("Table created successfully");

print("Opened database successfully")
conn.execute('''CREATE TABLE Charity
        (CharityID INT PRIMARY KEY     NOT NULL,
         CharityName TEXT    NOT NULL,
         CharityPhone TEXT     NOT NULL,
         CharityMail TEXT,
         CharityPassword TEXT,
         CharityAddress TEXT);''')
print("Table created successfully");

conn.close()