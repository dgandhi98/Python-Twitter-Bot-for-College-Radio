import requests as requests
from bs4 import BeautifulSoup
URL = 'http://thesting.wrur.org/schedule/'

def set_up_scraper():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser') 
    return soup

# Takes in a beautiful soup obj of a show
# Returns the time in string(XX:XX PM - XX:XX PM) and the parsed obj
def scrape_show(show):
    show_time = show.find_all(class_='show-time')[0].text
    show_name = show.find_all(class_='show-title')[0].text
    show_host = show.find_all(class_='show-host')[0].text

    obj = {}
    obj["show_type"] = "The Sting"
    obj["show_name"] = show_name
    obj["hosts"] = show_host

    return show_time, obj
    
# Formats hour for the key
def format_hour(hour, ampm):
    if ampm == 'PM' and hour == '12':
            return '12'
    elif ampm == 'AM' and hour == '12':
            return '0'
    elif ampm =='PM':
         return str( int(hour) + 12)
    else:
        return hour

# Formats the key from day and time 
# {sunday,...}, (XY{0-12}:ZZ PM - ZZ:ZZ PM) -> {Sun-XY{0-24},...}
def format_key(day, times):
    
    day = day[0:3].capitalize()

    start_time = times.split(' - ')[0]
    start_ampm = start_time.split(' ')
    start_hour = start_ampm[0].split(':')[0]

    return day + "-" + format_hour(start_hour, start_ampm[1])

# Creates whole object from an array of days
def create_obj(schedule):
    x = {}
    for each_day in schedule:
        curr_day = each_day['id']
        shows = each_day.div.find_all(class_='post')
        for show in shows:
            time, show_obj = scrape_show(show)
            x[format_key(curr_day, time)] = show_obj
    return x

soup_obj = set_up_scraper()
schedule = soup_obj.find_all(class_='tabs-content')[0].find_all(class_='content')
print(create_obj(schedule))
