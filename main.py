#!usr/bin/env python3

import tweepy
from datetime import datetime
import sys
import json
from pytz import timezone
import time
from os import environ

if 'consumer_key' in environ:
    consumer_key = environ['consumer_key']
    consumer_secret = environ['consumer_secret']
    access_token = environ['access_token']
    access_secret = environ['access_secret']
else:
    from auth import consumer_key, consumer_secret, access_token, access_secret

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# Create API Object
api = tweepy.API(auth)

# Check Functionality
try: 
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    sys.exit()

#api.update_status("Up and Running!")
#GLOBAL
eastern = timezone('US/Eastern')
with open('shows.json') as json_file:
    shows_data = json.load(json_file)
the_sting_link = "http://thesting.wrur.org/"
#FM_link = "https://www.wrur.org/"


#Gets the datetime in ET
def get_datetime_now_ET():
    return datetime.now(eastern)

#Formats hour for tweeting
def format_hour(hr_str):
    x = int(hr_str)%12
    if x == 0:
        return str(12)
    else: return str(x)

#the (vegan) meat
def main_procedure(curr_dt):
    in_15_mins = datetime.fromtimestamp(curr_dt.timestamp() + (15*60))
    shows_key = in_15_mins.strftime("%a-%H")
	
    if shows_key in shows_data:
        tshow = shows_data[shows_key]
        tweet_str = "Catch " + tshow["show_name"] \
            + " with " + tshow["hosts"] + " on " + tshow["show_type"] \
                + " at " + format_hour(in_15_mins.strftime("%H"))  + "!"	
                
        if tshow["show_type"] == "The Sting":
            tweet_str = tweet_str + "\n" + the_sting_link
#           elif tshow["show_type"]=="FM":
#           tweet_str = tweet_str + "\n" + FM_link
                
        if len(tweet_str) > 250:
            print(tshow["show_name"], " is too long.")
            tweet_str = "Catch a show on " +tshow["show_type"] +" in 15 minutes!"
        
        api.update_status(tweet_str) 
        time.sleep(1) # Let's wait a sec for the API

def to_be_called():
    #Keep running, call main_procedure to tweet at XX:45
    while True:
        currentDT = get_datetime_now_ET()
        
        main_procedure(currentDT)
        while int(currentDT.strftime("%M")) < 45:
            pass
        main_procedure(currentDT)
        time.sleep(15*60)

