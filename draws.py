import sys
import pandas as pd
import math
import matplotlib.pyplot as plt
import time
import numpy as np
from sklearn.cluster import DBSCAN


file = pd.read_csv(r'C:\Users\win\Desktop\new\Thesis\data\all.csv',
                   low_memory=False)  # reads the total data
df1 = pd.DataFrame(file)
df2 = df1[df1['CrowdLevel'] == 0]
df2 = df2.reset_index()

# values click on the DSCAM analysis array to mark the car identification that is ended on the same road to obtain information about the blocked section
cls = DBSCAN(eps=0.0001, min_samples=1).fit(
    df2[['longitude', 'latitude']].values)
n_clusters = len(set(cls.labels_))  # obtain the total number of congestion

# converts the congestion number into the dataframe
labels = pd.DataFrame(cls.labels_)
# add congested label to master data set
res = pd.concat([df2, labels], axis=1, ignore_index=True)
mylist = res[11].tolist()  # write the number of the congested section
res['Zone'] = None  # creates a new data column
myset = set(mylist)  # to get all blocked sections number
Num = []
for item in myset:  # calculate the total number of data points in a congested road section
    Num.append(mylist.count(item))
myset = list(myset)
c = {'myset': myset, 'Num': Num}
# deposit the congested section number and the number of data points under each number into the same
df_Ana = pd.DataFrame(c)
for item in df_Ana[df_Ana['Num'] > 500]['myset']:
    res.loc[res[11] == item, 'Zone'] = 1

res.columns = ['index1', 'index2', 'driver', 'order', 'time', 'longitude', 'latitude',
               'speed', 'CrowdLevel', 'wday', 'hour', 'labels', 'CrowdZone']  # update the header

res.to_csv(
    r'C:\Users\win\Desktop\new\Thesis\data\source_data\result.csv', encoding='gbk')


file = pd.read_csv(r'C:\Users\win\Desktop\new\Thesis\data\source_data\result.csv',
                   low_memory=False)  # read the data set of congested road after processing
res = pd.DataFrame(file)  # deposit the variable

Croad = res[res['CrowdZone'] == 1].drop_duplicates(subset='labels')[
    'labels'].tolist()
for item in Croad:  # map congested roads
    plt.scatter(res.loc[res['labels'] == item]['longitude'],
                res.loc[res['labels'] == item]['latitude'], s=60, c='b', alpha=0.5)
    plt.show()
