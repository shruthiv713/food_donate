import sqlite3
conn = sqlite3.connect('acms.db')
print("Opened database successfully")
conn.execute('''CREATE TABLE Hotel
        (HotelID INT PRIMARY KEY     NOT NULL,
         HotelName TEXT    NOT NULL,
         HotelPhone TEXT,
         HotelMail TEXT NOT NULL,
         HotelPassword TEXT NOT NULL,
         HotelAddress TEXT NOT NULL);''')
print("Table created successfully");

print("Opened database successfully")
conn.execute('''CREATE TABLE Charity
        (CharityID INT PRIMARY KEY     NOT NULL,
         CharityName TEXT    NOT NULL,
         CharityPhone TEXT ,
         CharityMail TEXT  NOT NULL,
         CharityPassword TEXT  NOT NULL,
         CharityAddress TEXT  NOT NULL);''')
print("Table created successfully");

conn.close()