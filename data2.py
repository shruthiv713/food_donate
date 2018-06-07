import pandas as pd
import numpy as np
import sqlite3
con = sqlite3.connect('acms.db')
con.row_factory = sqlite3.Row
cur = con.cursor()


df = pd.read_sql_query("select OrderPlaced.CharityID,OrderPlaced.AvailID,OrderPlaced.Rating,Availability.HotelID from OrderPlaced natural join Availability where Rating is not null;", con)

print(df)
print(df.info())

cha=pd.read_sql_query("select CharityID from Charity ;", con)
hote=pd.read_sql_query("select HotelID from Hotel ;", con)

cha=cha.values
hote=hote.values


print(cha)
print(hote)

print(cha.dtype)
print(hote.dtype)

df2 = pd.DataFrame(index=cha, columns=hote)
df2.fillna(0,inplace=True);


print(df2.shape)
print(df2.iloc[cha[0],hote[0]])





#df2=df2.values

#print(df2)

con.commit()
con.close()