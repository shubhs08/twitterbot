#importing the required libraries

import tweepy
import textblob
from textblob import TextBlob
import json
import paralleldots
import nltk
from nltk.corpus import stopwords
from collections import Counter
nltk.download('stopwords')

#Authentication part

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""
oauth=tweepy.OAuthHandler(consumer_key,consumer_secret)
oauth.set_access_token(access_token,access_token_secret)
api=tweepy.API(oauth)

# tweet with hashtag

def query():
    global tweets
    input = raw_input("Enter the tweet without hashtag")
    input = "#" + input
    tweets = api.search(q=input)

#structure of status object of tweet

def GetSearch():
    query()
    status = tweets[0]
    json_string = json.dumps(status._json,indent=4,sort_keys=True)
    print(json_string)

#followers count

def fcount():
    query()
    for tweet in tweets:
        print(tweet.user.name+"        "+str(tweet.user.followers_count))

#sentiment analyis

def sent_analysis():
    positive=0;
    negative=0;
    neutral=0;
    query()
    from paralleldots import set_api_key,sentiment
# Setting  API key
    set_api_key("F6IhnjekXoKsgzOwy1ZsGCX6ph76YK5F6SzFf968gOk")
#Viewing  API key
    paralleldots.get_api_key()
    for tweet in tweets:
        tweet_text=tweet.text
        sentiment_type=sentiment(tweet_text)
        sentiment_values=sentiment_type['sentiment']
        if sentiment_values=="positive":
            positive=positive+1;
        elif sentiment_values=="negative":
            negative=negative+1;
        else:
            neutral=negative+1;
    if positive>negative and positive>neutral:
        print("POSITIVE SENTIMENT with count"+ " "+str(positive))
    elif negative>positive and negative>neutral:
        print("NEGATIVE SENTIMENT with count" + " " +str(negative))
    else:
        print("NEUTRAL SENTIMNET with count" + " " +str(neutral))

#determining the location time zone and language

def location():
    global time_zone,location,language
    query()
    location_dict = {}
    language_dict = {}
    time_zone_dict = {}
    for tweet in tweets:
        location = tweet.user.location_dict
        language = tweet.user.lang_dict
        time_zone = tweet.user.time_zone_dict
        if location in location_dict:
            location_dict[location] += 1
        else:
            location_dict[location] = 1
        if language in language_dict:
            language_dict[language] += 1
        else:
            language_dict[language] = 1
        if time_zone in time_zone_dict:
            time_zone_dict[time_zone] += 1
        else:
            time_zone_dict[time_zone] = 1
    # limiting the display of the values
    if None in time_zone_dict:
        del time_zone_dict[None]
    if '' in time_zone_dict:
        del time_zone_dict['']
    if '' in language_dict:
        del language_dict['']
    if '' in location_dict:
        del location_dict['']
    if None in location_dict:
        del location_dict[None]
    if None in language_dict:
        del language_dict[None]
    language_count = dict(Counter(language_dict).most_common(5))
    print("Language:")
    print(language_count)
    location_count = dict(Counter(location_dict).most_common(5))
    print("Location:")
    print(location_count)
    time_zone_count = dict(Counter(time_zone_dict).most_common(5))
    print("Time Zone:")
    print(time_zone_count)

#comaprison of tweets

def compare():
    flagword = 0
    flagword1 = 0
    # for narendra modi
    tweets = api.user_timeline(screen_name="narendramodi", count=200, tweet_mode="extended")
    for tweet_compare in tweets:
        fulltext = tweet_compare.full_text
        tmp = []
        tmp.append(fulltext)
        temp = tmp
        import re
        cur_tweet = re.sub(r"http\S+", "", str(temp))
        cur_tweet = re.split(r"\s", cur_tweet)
        for word in cur_tweet:
            word=word.upper()
            if word == "AMERICA" or word == "US" or word=="USA" or word=="UNITED STATES OF AMERICA":
                flagword = flagword + 1
    print("USA BY NARENDRA MODI: "+ str(flagword))

    # for donald trump
    tweets = api.user_timeline(screen_name="realDonaldTrump", count=200, tweet_mode="extended")
    for tweet_compare in tweets:
        fulltext = tweet_compare.full_text
        tmp = []
        tmp.append(fulltext)
        temp = tmp
        import re
        cur_tweet = re.sub(r"http\S+", "", str(temp))
        cur_tweet = re.split(r"\s", cur_tweet)
        for word in cur_tweet:
            word = word.upper()
            if word == "INDIA" or word == "India" or word == "India":
                flagword1 = flagword1 + 1
    print("INDIA BY DONALD TRUMP: " + str(flagword1))

# analysing top usage

def top_usage():
    global count
    stop_words = set(stopwords.words('english'))
    x = [x.upper() for x in stop_words]
    tweets = api.user_timeline(screen_name="narendramodi", count=200, tweet_mode="extended")
    for tweet_compare in tweets:
        fulltext = tweet_compare.full_text
        tmp = []
        tmp.append(fulltext)
        temp = tmp
        import re
        cur_tweet = re.sub(r"http\S+", "", str(temp))
        cur_tweet1 = re.split(r"\s", cur_tweet)
        cur_tweet = [w for w in cur_tweet1 if not w in stop_words]
        cur_tweet=[]
        for w in cur_tweet1:
            if w not in stop_words:
                cur_tweet.append(w)
                count = Counter(cur_tweet).most_common(10)
        print(count)


#tweet a message

def tweet_status(new):
    message1 = raw_input("What do u want to update as a status?")
    api.update_status(message1)

#menu creation to select the options

show_menu=True
while show_menu==True:
     menu_choices = ("What do you want to do? \n1. Retrieve the tweets \n2. Count the followers \n3. Determine the sentiment \n4. Determine the location,language and time zone \n5. Comparison of the tweets \n6. Analyse the top usage \n7. Tweet a message \n8. Exit the application  ")
     menu_choice = raw_input(menu_choices)
     if menu_choice == "1":
         print('Retrieving the tweets')
         GetSearch()
     elif menu_choice == "2":
         print("counting the followers")
         fcount()
     elif menu_choice == "3":
         print("Determining the sentiments")
         sent_analysis()
     elif menu_choice == "4":
         print("Determining the location,language and time zone")
         location()
     elif menu_choice == "5":
         print("Comparing the tweets")
         compare()
     elif menu_choice == "6":
         print("Analysing the top usage")
         top_usage()
     elif menu_choice == "7":
         print("Tweeting a message")
         tweet_status(message1)
     else:
         show_menu = False





