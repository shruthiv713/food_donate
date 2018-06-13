import sqlite3
conn = sqlite3.connect('acms.db')

print("Opened database successfully")
conn.execute('''CREATE TABLE Availability
        (AvailID INTEGER PRIMARY KEY AUTOINCREMENT,
         HotelID INTEGER NOT NULL,
         AvailPeople INT ,
         AvailDT DATETIME DEFAULT (datetime('now','localtime')) ,
         ExpTime DATETIME NOT NULL,
         AvailLeftOut INT,
         FOREIGN KEY(HotelID) REFERENCES Hotel(HotelID));''')
print("Table created successfully");

print("Opened database successfully")
conn.execute('''CREATE TABLE OrderPlaced
        (OrderID INTEGER PRIMARY KEY  AUTOINCREMENT,
         CharityID INTEGER NOT NULL,
         AvailID INTEGER NOT NULL,
         People INT,
         Remaining INT,
         OrderTime DATETIME DEFAULT (datetime('now','localtime')),
         Rating INT,
         FOREIGN KEY(AvailID) REFERENCES Availability(AvailID),
         FOREIGN KEY(CharityID) REFERENCES Charity(CharityID)
         );''')

print("Table created successfully");




conn.close()