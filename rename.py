import sqlite3
conn = sqlite3.connect('acms.db')
print("Opened database successfully");

conn.execute('''ALTER TABLE OrderPlaced RENAME TO OrderPlaced_orig;''')
#ALTER TABLE team RENAME TO team_orig;
print("Table created successfully");

print("Opened database successfully");
conn.execute('''CREATE TABLE OrderPlaced
        (OrderID INTEGER PRIMARY KEY  AUTOINCREMENT,
         CharityID INTEGER NOT NULL,
         AvailID INTEGER NOT NULL,
         People INT,
         Remaining INT,
         OrderTime DATETIME DEFAULT (datetime('now','localtime')),
         FOREIGN KEY(AvailID) REFERENCES Availability(AvailID),
         FOREIGN KEY(CharityID) REFERENCES Charity(CharityID)
         );''')
#CREATE TABLE team(Name TEXT, Coach TEXT, Location TEXT);
print("Table created successfully");


print("Opened database successfully");
conn.execute('''INSERT INTO OrderPlaced(OrderID, CharityID, AvailID, People, Remaining, OrderTime) SELECT OrderID, CharityID, AvailID, People, Used, OrderTime FROM OrderPlaced_orig;''')
#INSERT INTO team(Name, Coach, Location) SELECT Name, Coach, City FROM team_orig;
print("Table created successfully");


print("Opened database successfully");
conn.execute('''DROP TABLE OrderPlaced_orig;''')
#DROP TABLE team_orig;
print("Table created successfully");



