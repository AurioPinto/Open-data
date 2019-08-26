import sys
import pandas as pd
import pandas as pd
import math
import matplotlib.pyplot as plt
import time
import numpy as np
from sklearn.cluster import DBSCAN


file = pd.read_csv(
    r'C:\Users\win\Desktop\new\Thesis\data\source_data\result.csv', low_memory=False)
df1 = pd.DataFrame(file)
df2 = df1[df1['CrowdZone'] == 1]
df2 = df2.reset_index()
df2.columns = ['index1', 'index2', 'index3', 'index4', 'driver', 'order', 'time', 'longitude',
               'latitude', 'speed', 'CrowdLevel', 'wday', 'hour', 'labels', 'CrowdZone']  # reset index
df2.to_csv(
    r'C:\Users\win\Desktop\new\Thesis\data\source_data\model.csv', encoding='gbk')


file = pd.read_csv(
    r'C:\Users\win\Desktop\new\Thesis\data\source_data\model.csv', low_memory=False)
model = pd.DataFrame(file)

model['Pre_Time'] = None  # new column

# Analyze  the congested situation of each crownded road section in each time period every day, and obtain the statistical model of the congestion time of this road section
model.drop_duplicates(subset={'wday', 'hour', 'labels'})
for item1 in model.drop_duplicates(subset='labels')['labels']:
    Temp = model[model['labels'] == item1]
    for item2 in Temp.drop_duplicates(subset='wday')['wday']:
        DayData = Temp[Temp['wday'] == item2].drop_duplicates(subset='hour')[
            'hour'].tolist()
        DayData.sort()
        for i in range(len(DayData)):
            for j in range(len(DayData)-i):
                if DayData[i]+j != DayData[i+j]:
                    model.loc[(model['labels'] == item1) & (model['wday'] == item2) & (
                        model['hour'] == DayData[i]), 'Pre_Time'] = j
                    break

model.to_csv(
    r'C:\Users\win\Desktop\new\Thesis\data\source_data\model.csv', encoding='gbk')


file = pd.read_csv(
    r'C:\Users\win\Desktop\new\Thesis\data\source_data\model.csv', low_memory=False)
model = pd.DataFrame(file)
lat = 30.67222
lng = 104.05914
hour = 15
wday = 1
for row in model.itertuples():
    print(getattr(row, 'Index'))
    if getDistance(lat, lng, getattr(row, 'latitude'), getattr(row, 'longitude')) < 100:
        RoadNum = getattr(row, 'labels')
        Pre_Time = getattr(row, 'Pre_Time')
        print('You are in the road of '+str(RoadNum) +
              ' and the predict time is '+str(Pre_Time))
        break
