## Imports
import requests
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

## Get ISS Position Data
def get_iss_position():
    url = "https://api.wheretheiss.at/v1/satellites/25544"
    response = requests.get(url, timeout=10)
    data = response.json()
    
    lat = data["latitude"]
    lon = data["longitude"]
    alt = data["altitude"]

    return(lat,lon,alt)

## Convert Lat, Lon, and Alt to Cartesian
def latlon2cart(lat,lon,alt):

    lat = np.radians(lat)
    lon = np.radians(lon)
    
    rad = 6371 + alt

    x = rad*np.cos(lat)*np.cos(lon)
    y = rad*np.cos(lat)*np.sin(lon)
    z = rad*np.sin(lat)

    return(x,y,z)

## Create Wireframe Earth
def wireframe(ax):

    u = np.linspace(0, 2*np.pi, 25)
    v = np.linspace(0, np.pi, 20)

    u,v = np.meshgrid(u,v)

    rad = 6371

    x = rad*np.cos(u)*np.sin(v)
    y = rad*np.sin(u)*np.sin(v)
    z = rad*np.cos(v)

    ax.plot_wireframe(x,y,z,color='w',linewidth=0.1)
    ax.set_box_aspect([1,1,1])
    ax.set_axis_off()

## Main Running
plt.ion()

fig = plt.figure(figsize=(8,8))
fig.patch.set_facecolor("k")
ax = fig.add_subplot(111, projection="3d")
wireframe(ax)

ax.view_init(elev=0, azim=0)
ax.set_facecolor("k")

lat,lon,alt = get_iss_position()
x,y,z = latlon2cart(lat,lon,alt)
iss_mark = ax.scatter(x,y,z,color="r",s=1.5)

ax.scatter(0,0,6731,color="y",s=10)
ax.text(0,0,6731+500,"North Pole",color="y")

ax.scatter(0,0,-6731,color="y",s=10)
ax.text(0,0,-6731-1200,"South Pole",color="y")

xl,yl,zl = latlon2cart(51.5,0,0)
london_mark = ax.scatter(xl,yl,zl,color="b",s=10)

time.sleep(10)

while True:
    lat, lon, alt = get_iss_position()
    print("Lat|Lon: ", str(lat), "|", str(lon))
    x, y, z = latlon2cart(lat, lon, alt)

    ax.scatter(x, y, z, color="r", s=1.5)

    plt.pause(10)