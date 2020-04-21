import pyodbc 
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

#Connecting to SQL Server
server_name = "DESKTOP-5F0PH62\SQLEXPRESS"
db_name = "Youtube_Trend_DW_ALL"

server = "Server="+str(server_name)
db = "Database="+str(db_name)
key = "Driver={SQL Server Native Client 11.0};"+server+";"+db+";"+"Trusted_Connection=yes;"

cnxn = pyodbc.connect(key)

sql= """
    
    select Top 50 Title as Videos,Likes,Most_Watched,Country,Category,Year_ as Year  from Trends_Fact as T
    inner join Video_DIM as V
    on v.VideoKey=T.VideoKey
    inner join Channel_DIM as C
    on C.ChannelKey=T.ChannelKey
    inner join Date_DIM as D
    on D.DateKey = T.DateKey
    Where  Top_Rated>80000 
    order by Top_Rated desc
"""
df=pd.read_sql(sql, cnxn)
df.head(50)

x1=np.array(df['Likes'])
x2=np.array(df['Most_Watched'])

x3=np.array(df['Country'])
x4=np.array(df['Category'])

#Scattered Plot
plt.plot()
plt.title('Youtube Dataset')
plt.scatter(x1,x2)
plt.show()

plt.plot()
plt.title('Most Watched videos by category')
plt.scatter(x3,x4)
plt.xlabel('Country')
plt.ylabel('Category')
plt.show()

#Numpy Zip method
x=np.array(list(zip(x1,x2)))
colors = ['b','g','r']
markers = ['o','v','s']

plt.xlabel('Likes')
plt.ylabel('Most_Watched')

kmeans= KMeans(n_clusters=3).fit(x)

plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], s=200, c='Black', label='Trends')

for i,j in enumerate(kmeans.labels_):
    plt.plot(x1[i], x2[i], color=colors[j], marker= markers[j])

plt.legend()
plt.show()
