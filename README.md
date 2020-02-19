# WRUR-Bot

## Introduction
A Twitter Bot to send out tweets when a show on our online college radio station is about to start.
Tweeting at https://twitter.com/ShowsWrur

## Dependencies
- Running on Python 3.8
- Currently running on AWS Lambda
- Tweepy (Python Wrapper API for the Twitter API)
- Beautiful Soup (Used for scraping data)
- pytz (Used for TimeZone functionalities)


## Basic Functionality
Using CloudWatch Events on AWS Lambda, the main.lambda_handler function is scheduled to:
1. scrape data from our [college radio website](thesting.wrur.org), 
2. check whether a radio show is about to start (in 15 minutes, at the hour),
3. and then send out a tweet if the latter is the case.
