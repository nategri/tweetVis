#!/usr/bin/python

import twitter
import MySQLdb
import sys
import datetime
import pytz
import time

# Performs search and logs results in MySQL database
def performSearch(max_tweet_id = None):

  if max_tweet_id == None:
    searchResultList = myApiAccess.GetSearch(geocode=("37.7833","-122.4167","10mi"),result_type="recent",count=100)
  else:
    searchResultList = myApiAccess.GetSearch(geocode=("37.7833","-122.4167","10mi"),result_type="recent",count=100,max_id=max_tweet_id)

  
  for result in searchResultList:

    if result.coordinates != None:
      tweet_id = result.id
      username = result.user.name
      realname = result.user.screen_name
      latitude = result.coordinates['coordinates'][1]
      longitude = result.coordinates['coordinates'][0]
      favorites = result.favorite_count
      content = result.text

      # Time needs a little care to work with MySQL correctly

      # Stupid bug in this version of Python means I need to remove the timezone
      slicedTime = result.created_at.split(' ')
      slicedTime.pop(4)
      newTime = ' '.join(slicedTime)
      parsedTime = datetime.datetime.strptime(newTime,"%a %b %d %H:%M:%S %Y")
      # Implementing timezone handling. Thank you random strangers with blogs.
      myDate = pytz.timezone("UTC").localize(parsedTime)
      time = myDate.astimezone(pytz.timezone("US/Pacific")).strftime("%Y-%m-%d %H:%M:%S")

      links = ""
      hashtags = ""
      medialink = ""
      if len(result.media) > 0:
        if result.media[0]['type'] == 'photo':
          medialink =  result.media[0]['display_url']
      for link in result.urls:
        links = links + str(link.expanded_url)
      links = links + " " + medialink
      for subject in result.hashtags:
        hashtags = hashtags + subject.text.encode('ascii','ignore')+" "

      myCursor.execute("""INSERT INTO sanfrancisco (tweet_id,username,realname,time,content,favorites,links,hashtags,latitude,longitude)
                          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",(tweet_id,username,realname,time,content,favorites,links,hashtags,latitude,longitude))

  # Maybe sometimes the last id isn't actually the smallest?
  """min_id = searchResultList[-1].id
  for result in searchResultList:
    if result.id < min_id:
      min_id = result.id"""

  if len(searchResultList) == 0:
    return None
  else:
    return searchResultList[-1].id


# Read in Twitter authorization info
twaccess_file = open('nategri.twaccess','r')

twaccess_lines = twaccess_file.readlines()

myConsumerKey = twaccess_lines[0].replace("\n","")
myConsumerSecret = twaccess_lines[1].replace("\n","")
myAccessTokenKey = twaccess_lines[2].replace("\n","")
myAccessTokenSecret = twaccess_lines[3].replace("\n","")

twaccess_file.close()

# Create object through which Twitter API access occurs
myApiAccess = twitter.Api(consumer_key = myConsumerKey,
                          consumer_secret = myConsumerSecret,
                          access_token_key = myAccessTokenKey,
                          access_token_secret = myAccessTokenSecret)

# Create objects through which MySQL database access occurs
myDatabase = MySQLdb.connect("localhost","nategri","hermetic","geo_tweets",charset="utf8",use_unicode=True)
myCursor = myDatabase.cursor()

#myCursor.execute("DROP TABLE sanfrancisco;")

# Initialize my database
myCursor.execute("""CREATE TABLE sanfrancisco (tweet_id BIGINT UNSIGNED NOT NULL PRIMARY KEY,
                                                     username VARCHAR(40),
                                                     realname VARCHAR(40),
                                                     time DATETIME,
                                                     content TEXT,
                                                     favorites INT UNSIGNED,
                                                     links TEXT,
                                                     hashtags TINYTEXT,
                                                     latitude TINYTEXT,
                                                     longitude TINYTEXT);""")

myCursor.execute("SET CHARACTER SET utf8;""")

# Loop recursively through search results
last_id = None

while True:

  print("Performing searches....")

  for i in range(160):

    if last_id != None:
      last_id = last_id - 1
  
    last_id = performSearch(last_id)

    if last_id == None:
      break
  
  myDatabase.commit()

  if last_id == None:
    print("Welp looks like we're done here.")
    break

  print("Sleeping...")
  
  for i in range(16):
    if i == 14:
      print("Two minute warning! Searches will resume.")
    time.sleep(60)
  
