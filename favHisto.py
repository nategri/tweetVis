#!/usr/bin/python

import MySQLdb

import sys
import matplotlib.pyplot as plotter

# Create database objects
myDatabase = MySQLdb.connect("localhost","nategri","hermetic","geo_tweets",charset="utf8",use_unicode=True)
myCursor = myDatabase.cursor()


# Assemble a query from command line input
myQuery = "SELECT favorites FROM sanfrancisco WHERE "+ sys.argv[1] + ";"

myCursor.execute(myQuery)

queryResult = myCursor.fetchall()

favArray = []

for result in queryResult:
  favArray.append(result[0])

#print(favArray)

#myBins = [-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5]
#myBins = [-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5]

plotter.xlim(-0.5,20.5)

plotter.xlabel("Favorites")
plotter.ylabel("No. of Tweets")

plotter.hist(favArray,21,(-0.5,20.5),histtype="bar", rwidth=0.5, color="gold")

plotter.title(sys.argv[2])

#plotter.show()

plotter.savefig("histo.png")
