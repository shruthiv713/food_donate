import sqlite3
conn = sqlite3.connect('acms.db')
print("Opened database successfully");
conn.execute('''ALTER TABLE OrderPlaced ADD column Rating real;''')
print("Table created successfully");



conn.commit();
conn.close()