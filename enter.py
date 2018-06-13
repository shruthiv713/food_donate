import sqlite3
conn = sqlite3.connect('acms.db')

print("Opened database successfully")

#conn.execute('''INSERT INTO Hotel VALUES (1,'A2B','9444348018','a2b@gmail.com','test@user1','a2b');''')
#conn.execute('''INSERT INTO Hotel (HotelName,HotelMail,HotelPassword,HotelAddress) VALUES ('hotchips','hotchips@gmail.com','test@user2','hotchips');''')

#conn.execute('''INSERT INTO Charity VALUES (1,'Mother Teresa','9488524574','motherteresa@gmail.com','test@userc1','Mother Teresa');''')

#conn.execute('''INSERT INTO Availability (HotelID,AvailPeople,ExpTime) VALUES (1,20,'2018-05-06 10:00:00');''')

conn.execute('''INSERT INTO OrderPlaced (CharityID,AvailID,People) VALUES (1,2,25);''')


conn.commit()
#conn.execute('''INSERT INTO Charity (CharityName,CharityMail,CharityPassword,CharityAddress) VALUES ('Hope Public','hope@gmail.com','test@userc2','Hope');''')

#conn.execute('''INSERT INTO Availability (HotelID,AvailPeople,ExpTime) VALUES (2,30,'2018-05-06 10:00:00');''')

conn.execute('''INSERT INTO OrderPlaced (CharityID,AvailID,People) VALUES (2,1,17);''')

conn.commit()


print("Table created successfully");

conn.close()