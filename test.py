import sys
import pandas as pd
import math
import matplotlib.pyplot as plt
import time
import numpy as np
from sklearn.cluster import DBSCAN


EARTH_REDIUS = 6378.137
pi = 3.14
level1 = 10
level2 = 15
level3 = 25
level4 = 35


def rad(d):
    return d * pi / 180.0


# calculate the distance between the points,the distance of the surface , is obtained by conversion of longitude and latitude
def getDistance(lat1, lng1, lat2, lng2):
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) +
                                math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b/2), 2)))
    s = s * EARTH_REDIUS
    return s


file = pd.read_csv(
    r'C:\Users\win\Desktop\new\Thesis\data\source_data\gps_20161101.csv')
df = pd.DataFrame(file)
df['velosity'] = None  # new data column
df['CrowdLevel'] = None  # new data column
df['tm_wday'] = None  # new data column
df['tm_hour'] = None  # new data column
lng1 = df.iloc[0, 3]  # initializes the longitude variable
lat1 = df.iloc[0, 4]  # initializes the latitude variable
time1 = df.iloc[0, 2]  # initializes the time variable
lng2 = df.iloc[0, 3]
lat2 = df.iloc[0, 4]
time2 = 0
print(df.iloc[0])


for row in df.itertuples():
    print(getattr(row, 'Index'))
    # get the new longitude of the current row
    lng2 = getattr(row, 'longitude')
    lat2 = getattr(row, 'latitude')  # get the new latitude of the current row
    time2 = getattr(row, 'time')
    lng1 = lng2  # sending token
    lat1 = lat2  # generation values
    time1 = time2  # send generation assignment
    try:
        # calculate the vehicle driving speed
        velosity = abs(getDistance(lat1, lng1, lat2, lng2)/(time2-time1))*3600
    except ZeroDivisionError:
        velosity = 0

    df.iloc[getattr(row, 'Index'), 5] = velosity
    if velosity > level4:
        df.iloc[getattr(row, 'Index'), 6] = 4
    elif velosity > level3:
        df.iloc[getattr(row, 'Index'), 6] = 3
    elif velosity > level2:
        df.iloc[getattr(row, 'Index'), 6] = 2
    elif velosity > level1:
        df.iloc[getattr(row, 'Index'), 6] = 1
    else:
        df.iloc[getattr(row, 'Index'), 6] = 0
    timestamp = getattr(row, 'time')
    time_local = time.localtime(timestamp)
    df.iloc[getattr(row, 'Index'), 7] = time_local.tm_wday  # current time
    df.iloc[getattr(row, 'Index'), 8] = time_local.tm_hour
df.to_csv(
    r'C:\Users\win\Desktop\new\Thesis\data\source_data\gps_20161101.csv', encoding='gbk')
