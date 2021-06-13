#!/usr/bin/env python
# coding: utf-8

# ## Problem 3: How long distance individuals have travelled? 
# 
# In this problem the aim is to calculate the "distance" in meters that the individuals have travelled according the social media posts (Euclidean distances between points). In this problem, we will need the `userid` -column an the points created in the previous problem. You will need the shapefile `Kruger_posts.shp` generated in Problem 2 as input file.
# 

# YOUR CODE HERE 1 to read data
import geopandas as gpd
from pyproj import CRS
data=None
# read the data 'Kruger_posts.shp' 
data=gpd.read_file('Kruger_posts.shp')
# - Check the crs of the input data. If this information is missing, set it as epsg:4326 (WGS84).
# - Reproject the data from WGS84 to `EPSG:32735` -projection which stands for UTM Zone 35S (UTM zone for South Africa) to transform the data into metric system. (don't create a new variable, update the existing variable `data`!)"

# YOUR CODE HERE 2 to set crs
# change data to use to_crs
data = data.to_crs(epsg=32735)
# CODE FOR TESTING YOUR SOLUTION

# Check the data
print(data.head())

# CODE FOR TESTING YOUR SOLUTION

# Check that the crs is correct after re-projecting (should be epsg:32735)
print(data.crs)


#  - Group the data by userid

#  YOUR CODE HERE 3 to group 
grouped=None
# group data
grouped = data.groupby('userid')
# CODE FOR TESTING YOUR SOLUTION

#Check the number of groups:
assert len(grouped.groups) == data["userid"].nunique(), "Number of groups should match number of unique users!"


# **Create LineString objects for each user connecting the points from oldest to latest:**
# 

# YOUR CODE HERE 4 to set movements
import pandas as pd
from shapely.geometry import LineString, Point
movements=None
# create dataframe called movement to use GeoDataFtame and  setup column 'userid''geometry'
movements = gpd.GeoDataFrame(columns=['userid','geometry'])
a = 0
for key, group in grouped:
    group = group.sort_values('timestamp')
    if len(group['geometry'])>=2:
        line = (LineString(list(group['geometry'])))
    else:
        line=None
    a +=1
    movements.at[a, 'userid'] = key
    movements.at[a, 'geometry'] = line
movements.crs = CRS.from_epsg(32735)

# CODE FOR TESTING YOUR SOLUTION

#Check the result
print(type(movements))
print(movements.crs)
print(movements["geometry"].head())


# **Finally:**
# - Check once more the crs definition of your dataframe (should be epsg:32735, define the correct crs if this information is missing)
# - Calculate the lenghts of the lines into a new column called ``distance`` in ``movements`` GeoDataFrame.

# YOUR CODE HERE 5 to calculate distance
# for sentenses to calculate distance
def cal_distance(x):
  if x['geometry'] is None:
    return None
  else:
    return x['geometry'].length
movements['distance'] = movements.apply(cal_distance, axis=1)

# CODE FOR TESTING YOUR SOLUTION

#Check the output
movements.head()


# You should now be able to print answers to the following questions: 
# 
#  - What was the shortest distance travelled in meters?
#  - What was the mean distance travelled in meters?
#  - What was the maximum distance travelled in meters?

# YOUR CODE HERE 6 to find max, min,mean of the distance.
from statistics import mean
print(mean(movements['distance']))
print(max(movements['distance'].dropna()))
print(min(movements['distance']))

# - Finally, save the movements of into a Shapefile called ``some_movements.shp``

# YOUR CODE HERE 7 to save as Shapefile
# save the file 'some_movements.shp
fp='some_movements.shp'
movements.to_file(fp)

# CODE FOR TESTING YOUR SOLUTION

import os

#Check if output file exists
assert os.path.isfile(fp), "Output file does not exits."


# That's all for this week!
#check length
def func7():
    return data

#check type
def func8():
    return grouped 

#check crs
def func9():
    return movements

#check movements['distance']
def func10():
    return movements