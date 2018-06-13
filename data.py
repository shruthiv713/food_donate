import pandas as pd
import numpy as np
import sqlite3
con = sqlite3.connect('acms.db')
con.row_factory = sqlite3.Row
cur = con.cursor()

df = pd.read_sql_query("select OrderPlaced.CharityID,OrderPlaced.AvailID,OrderPlaced.Rating,Availability.HotelID from OrderPlaced natural join Availability where Rating is not null;", con)
#df=pd.read_sql_query("select OrderPlaced.CharityID,OrderPlaced.AvailID,OrderPlaced.Rating,Availability.HotelID from OrderPlaced ,Availability ;", con)

print(df)

#df2=pd.read_sql_query("select HotelID,AvailID from Availability where AvailID in (select AvailID from OrderPlaced where Rating is not null);", conn)
#print(df2)

#cur.execute('''select CharityID from Charity ;''')
#cha=pd.read_sql_query("select CharityID from Charity ;", con)
#chamat=cha.as_matrix();

#cur.execute('''select HotelID from Hotel ;''')
#hote=pd.read_sql_query("select HotelID from Hotel ;", con)
#hotemat=hote.as_matrix();

#print(chamat)
#print(hotemat)
#print(df.iloc[1]['CharityID'].type)
#print(df.get_value(1,'CharityID'))

#df2 = pd.DataFrame(index=cha, columns=hote)
#df2.fillna(0);
#print(df2.shape)

print(df.info())


#for row in df.itertuples():
    #print(row[1])
    #print(row[4])
    #print(row[3])
    #df2.iloc[row[1],row[4]]=row[3]
    #print(df2.iloc[1,2])


R_df = df.pivot(index = 'CharityID', columns ='HotelID', values = 'Rating').fillna(0)
print(R_df.head())
R = R_df.as_matrix()
user_ratings_mean = np.mean(R, axis = 1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)


from scipy.sparse.linalg import svds
U, sigma, Vt = svds(R_demeaned, k = 5)

sigma = np.diag(sigma)


all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns = R_df.columns)
print(preds_df.head())

sorted_user_predictions = preds_df.iloc[0].sort_values(ascending=False)

print(sorted_user_predictions)

#print(df2.head())

con.commit()
con.close()