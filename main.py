#!usr/bin/env python3

import tweepy
from datetime import datetime
import sys
import json
from pytz import timezone
import time
import scraper
from authent import consumer_key, consumer_secret, access_token, access_secret

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
the_sting_link = "http://thesting.wrur.org/"

#Gets the datetime in ET
def get_datetime_now_ET():
    return datetime.now(eastern)

#Formats hour for tweeting
def str_format_hour(hr_str):
    x = int(hr_str)%12
    if x == 0:
        return str(12)
    else: return str(x)

#the (vegan) meat
def main_procedure(curr_dt, shows_data):
    # Find out the time in 15 minutes, make sure to keep in Eastern Timezone!
    in_15_mins = datetime.fromtimestamp(curr_dt.timestamp() + (15*60))
    in_15_mins = in_15_mins.astimezone(eastern)
    shows_key = in_15_mins.strftime("%a-%H")

    print("before adding: ", curr_dt.strftime("%a-%H"))
    print("shows key: ", shows_key)
    print("shows data: ", shows_data)
    
    # Have we got a show in 15 minutes?
    if shows_key in shows_data and shows_key != curr_dt.strftime("%a-%H"):
        tshow = shows_data[shows_key]
        tweet_str = "Catch " + tshow["show_name"] \
            + " with " + tshow["hosts"] + " on " + tshow["show_type"] \
                + " at " + str_format_hour(in_15_mins.strftime("%H"))  + "!"	
                
        if tshow["show_type"] == "The Sting":
            tweet_str = tweet_str + "\n" + the_sting_link
                
        if len(tweet_str) > 250:
            print(tshow["show_name"], " is too long.")
            tweet_str = "Catch a show on " +tshow["show_type"] +" in 15 minutes!" + "\n"\
                    + the_sting_link
        
        api.update_status(tweet_str) 
        print("Sent Tweet: ", tweet_str)
        time.sleep(1) # Let's wait a sec for the API

def lambda_handler(_event_json, _context):
    currentDT = get_datetime_now_ET()
    shows_data = scraper.scrape()
    main_procedure(currentDT, shows_data)

'''
def main():
    #lambda_handler('','')
    shows_data = scraper.scrape()
    main_procedure(datetime.datetime(2020, 5, 1))
if __name__=="__main__":
    main()
'''

