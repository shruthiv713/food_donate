import sqlite3
conn = sqlite3.connect('acms.db')
print("Opened database successfully");
conn.execute('''DROP TABLE OrderPlaced''')
print("Table created successfully");

print("Opened database successfully");
conn.execute('''DROP TABLE Availability''')
print("Table created successfully");

print("Opened database successfully");
conn.execute('''DROP TABLE Charity''')
print("Table created successfully");

print("Opened database successfully");
conn.execute('''DROP TABLE Hotel''')
print("Table created successfully");

conn.close()