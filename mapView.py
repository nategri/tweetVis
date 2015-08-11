#!/usr/bin/python

# bounds of map in latitude and the longitude

# 39.8621 - 40.1196
# -83.1541 - -82.8232

import MySQLdb
import sys
import matplotlib.pyplot as plotter

import matplotlib.markers as pts

# Minimum/Maximum latitude and longitude on the map
# Columbus
#minLat = 39.8621
#maxLat = 40.1196
#minLong = -83.1541
#maxLong = -82.8232

# San Francisco
minLat = 37.6816
maxLat = 37.8145
minLong = -122.5188
maxLong = -122.3534

# Create database objects
myDatabase = MySQLdb.connect("localhost","nategri","hermetic","geo_tweets",charset="utf8",use_unicode=True)
myCursor = myDatabase.cursor()

# Setup plot
mapfile = plotter.imread("tweetsanfranciscobw.png")
mapscatter = plotter.imshow(mapfile, extent=(minLong,maxLong,minLat,maxLat))

plotter.ylim(minLat,maxLat)
plotter.xlim(minLong,maxLong)

plotter.title("Location Tagged Tweets in San Franciso, CA")

#myFigure, myAxis = plotter.subplot()

myAxis = plotter.gca()
myAxis.get_xaxis().set_visible(False)
myAxis.get_yaxis().set_visible(False)

vanillaQuery = """SELECT latitude, longitude FROM sanfrancisco WHERE (links NOT LIKE '%instagram.com%') AND (links NOT LIKE '%swarmapp.com%')
                    AND (links NOT LIKE '%pic.twitter.com%') AND (links NOT LIKE '%4sq.com%') AND ("""

instagramQuery = "SELECT latitude, longitude FROM sanfrancisco WHERE links LIKE '%instagram.com%' AND ("

swarmQuery = "SELECT latitude, longitude FROM sanfrancisco WHERE links LIKE '%swarmapp.com%' AND ("

twitterpicQuery = "SELECT latitude, longitude FROM sanfrancisco WHERE (links LIKE '%pic.twitter.com%') AND (favorites >= 0) AND ("

foursquareQuery = "SELECT latitude, longitude FROM sanfrancisco WHERE (links LIKE '%4sq.com%') AND (favorites >= 0) AND ("

def plotTweets(query,color,timearg):
  query = query + timearg + ");"
  myCursor.execute(query)
  while True:
    currTuple = myCursor.fetchone()
    if currTuple == None:
      break
    x_array = float(currTuple[1])
    y_array = float(currTuple[0])
    plotter.scatter(x_array,y_array, s=30, c=color, marker=".", edgecolors = 'none')

if (sys.argv[1] == "vanilla") or (sys.argv[1] == "all"):
  print("Plotting vanilla tweets...")
  plotTweets(vanillaQuery,"teal",sys.argv[2])

if (sys.argv[1] == "instagram") or (sys.argv[1] == "all"):
  print("Plotting Instagram tweets...")
  plotTweets(instagramQuery,"brown",sys.argv[2])

if (sys.argv[1] == "swarm") or (sys.argv[1] == "all"):
  print("Plotting Swarm tweets...")
  plotTweets(swarmQuery,"orange",sys.argv[2])

if (sys.argv[1] == "twitterpic") or (sys.argv[1] == "all"):
  print("Plotting Twitter Picture tweets...")
  plotTweets(twitterpicQuery,"blue",sys.argv[2])

if (sys.argv[1] == "foursquare") or (sys.argv[1] == "all"):
  print("Plotting Foursquare tweets...")
  plotTweets(foursquareQuery,"red",sys.argv[2])

vanilla_pts = plotter.scatter([], [], c='teal', marker=".", s=60, edgecolors = 'none', label='Vanilla')
insta_pts = plotter.scatter([], [], c='brown', marker=".", s=60, edgecolors = 'none', label='Instagram')
swarm_pts = plotter.scatter([], [], c='orange', marker=".", s=60, edgecolors = 'none', label='Swarm')
foursq_pts = plotter.scatter([], [], c='red', marker=".", s=60, edgecolors = 'none', label='Foursquare')
twitterpic_pts = plotter.scatter([], [], c='blue', marker=".", s=60, edgecolors = 'none', label='Twitter Pic')

plotter.legend(handles=[vanilla_pts,insta_pts,swarm_pts,foursq_pts,twitterpic_pts], bbox_to_anchor=(0.0,-.10,1.0,-0.1), loc=4, ncol=3, mode="expand", borderaxespad=0)

plotter.title(sys.argv[3])

plotter.savefig("tweetmap.png",dpi=120)
