import sqlite3
conn = sqlite3.connect('acms.db')

print("Opened database successfully")
conn.execute('''CREATE TABLE Availability
        (AvailID INT PRIMARY KEY NOT NULL,
         HotelID INT NOT NULL,
         AvailPeople INT ,
         AvailTime TIME ,
         ExpTime TIME NOT NULL,
         FOREIGN KEY(HotelID) REFERENCES Hotel(HotelID));''')
print("Table created successfully");





print("Opened database successfully")
conn.execute('''CREATE TABLE OrderPlaced
        (OrderID INT PRIMARY KEY  NOT NULL,
         CharityID INT NOT NULL,
         AvailID INT NOT NULL,
         People INT,
         Used INT,
         OrderTime TIME,
         FOREIGN KEY(AvailID) REFERENCES Availability(AvailID),
         FOREIGN KEY(CharityID) REFERENCES Charity(CharityID)
         );''')

print("Table created successfully");




conn.close()