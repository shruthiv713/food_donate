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

cha=cha.transpose()
hote=hote.transpose()

cha.flatten()
hote.flatten()

print(cha.shape)
print(hote.shape)


print(cha)
print(hote)

print(cha.dtype)
print(hote.dtype)

print(cha.__class__)
print(hote.__class__)

df2 = pd.DataFrame(index=cha[0], columns=hote[0],dtype=np.float64)
df2.fillna(0,inplace=True);
count=pd.DataFrame(index=cha[0], columns=hote[0],dtype=np.int32)
count.fillna(0,inplace=True)


print(df2.shape)
#df2.set_value(15,1,2)
print(df2.get_value(15,1))
print(df2)





for row_index,row in df.iterrows():
    #print(row_index)
    #print("charityid")
    #print(int(row['CharityID']))
    #print("hotelid")
    #print(int(row['HotelID']))
    #print(int(row[0]))
    #df2.iloc[int(row['CharityID']),int(row['HotelID'])]
    val=(count.get_value(int(row['CharityID']),int(row['HotelID']))*df2.get_value(int(row['CharityID']),int(row['HotelID']))+float(row['Rating']))/(count.get_value(int(row['CharityID']),int(row['HotelID']))+1)
    df2.set_value(int(row['CharityID']),int(row['HotelID']),float(val))
    count.set_value(int(row['CharityID']),int(row['HotelID']),count.get_value(int(row['CharityID']),int(row['HotelID']))+1)











#df2=df2.values

print(df2)


R=df2.as_matrix()
user_ratings_mean = np.mean(R, axis = 1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)



from scipy.sparse.linalg import svds
U, sigma, Vt = svds(R_demeaned, k = 5)

sigma = np.diag(sigma)


all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns = df2.columns)
print(preds_df.head())

ind=np.where(cha[0]==1)
print(ind[0])
sorted_user_predictions = preds_df.iloc[int(ind[0])].sort_values(ascending=False)


print(sorted_user_predictions)

greaterz=sorted_user_predictions[sorted_user_predictions> 0]

print(greaterz.__class__)

print(greaterz)
print(greaterz.index)

rechot=greaterz.index

#for i in range(0,rechot.size):
#placeholder= '?' # For SQLite. See DBAPI paramstyle.
#placeholders= ', '.join(placeholder for unused in rechot)
sql="select HotelName,AvailLeftOut,ExpTime,AvailID,Hotel.HotelID from  Availability natural join Hotel where AvailLeftOut > 0 and ExpTime > datetime('now','localtime') and Hotel.HotelID in {}".format(str(tuple(rechot)))
   #cur.execute("select HotelName,AvailLeftOut,ExpTime,AvailID,Hotel.HotelID from  Availability natural join Hotel where AvailLeftOut > 0 and ExpTime > datetime('now','localtime') and Hotel.HotelID='{}'".format(i) )
cur.execute(sql)
orderrows = cur.fetchall();
print(orderrows)









con.commit()
con.close()