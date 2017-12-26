
# coding: utf-8

# In[7]:


import requests
import re
import tweepy
import pprint
from tweepy import OAuthHandler
import numpy as np
import pandas as pd


# In[2]:


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, ibmUserName, ibmPassword, ibmUrl):
        '''
        Class constructor or initialization method.
        '''
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
            self.ibmUserName = ibmUserName
            self.ibmPassword = ibmPassword
            self.ibmUrl = ibmUrl
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        route = '/v3/tone'
        fullURL = self.ibmUrl + route
        headers = {
            "Content-Type" : "application/json",
        }
        auth = (self.ibmUserName, self.ibmPassword)
        params = {
            "version" : "2017-09-21",
            'text' : self.clean_tweet(tweet)
        }
        analysis = requests.get(params=params, headers=headers, url=fullURL, auth=auth)
        print("Status Code: {0}; Reason: {1}".format(analysis.status_code, analysis.reason))
        return(analysis.json())
 
    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


# In[4]:


def getCreds():
    creds = {}
    longString = '''    M.......MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM8............,MMMMM.......MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    ..~+++...MMMMMMMMMMMMMMMMMMMMMMMMMMMMM..++++..++++..:MMM...+++:..MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    ..+++++.......:MMMMMMMMMMMMMMMMMMMMMM8..++++:.++++=..MMM..+++++..MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    ..+++++...............MMM.....?MM=.......++,..++++=..ZZZ..+++++..OZZMMMMO........,NMMMMD.. ......~MM
    ..++++++++++++++..++...7..=++......++=........++++=.......+++++.......,...,++++=....8$...,++++++...M
    ..++++++++++++++.++++....=++++....++++:.++++..+++++++++++.+++++++++++...+++++++++++....++++++++++..N
    ..+++++=======,..++++....=++++....++++:.++++:.+++++++++++.+++++++++++=.+++++,.,+++++..++++++++++~..M
    ..+++++..........++++....=++++....++++:.++++~.++++++++++..=+++++++++~.~+++++++++++++:+++++........MM
    ..+++++.... .....++++....+++++....++++,.++++~.+++++.......,++++.......=+++++++++++++.++++=..MMMMMMMM
    ..~++++++++++++..++++++:+++++++==+++++..++++~..+++++++++...+++++++++:..++++=....,=+,.++++=..MMMMMMMM
    M..:++++++++++++..+++++++++++++++++++...++++~..:+++++++++...?++++++++=..+++++++++++=.++++=..MMMMMMMM
    MM...++++++++++~....+++++++.~++++++:....++++.....++++++++....~+++++++....:++++++++...,+++...MMMMMMMM
    MMMN.............M,..................M8......~M$..........$M...........M...........:.......MMMMMMMMM
    MMMMMMM8?+++++ZMMMMMMN7+ZMMMMMD+?DMMMMMMM7?MMMMMMMMO+++IMMMMMMMN7+++NMMMMMMN7+IDMMMMMM8+8MMMMMMMMMMM
    '''
    print(longString)
    print("---------------------------------------------------------")
    print("Twitter Credentials: ")
    creds["consumerKey"] = input("Enter Twitter consumer key: \n")
    creds["consumerSecret"] = input("Enter Twitter consumer secret: \n")
    creds["accessToken"] = input("Enter Twitter access token: \n")
    creds["tokenSecret"] = input("Enter Twitter access token secret: \n")
    print("---------------------------------------------------------")
    print("---------------------------------------------------------")
    print("IBM Credentials: ")
    creds["ibmUsername"] = input("Enter IBM username: \n")
    creds["ibmPassword"] = input("Enter IBM password: \n")
    creds["ibmURL"] = input("Enter IBM URL: \n")
    print("---------------------------------------------------------")
    return(creds)


# In[4]:


def getTweets(creds):
    print("")
    api = TwitterClient(creds['consumerKey'], creds['consumerSecret'], creds['accessToken'], creds['tokenSecret'], creds['ibmUsername'], creds['ibmPassword'], creds['ibmURL'])
    targetEntity = input("Enter the query to search tweets: \n")
    count = input("Enter the number of tweets to analyse: \n")
    tweets = api.get_tweets(query = targetEntity, count = count)
    iterationCount = 0
    for tweet in tweets:
        iterationCount = iterationCount + 1
        if(iterationCount>10):
            print("Too many tweets, please wait while final output is generated...")
            break
        try:
            print("Tweet: {0}".format(tweet['text']))
        except:
            print("**********Tweet contained un-printable content (emoji)**********")
        if(len(tweet['sentiment']['document_tone']['tones']) == 0):
            print("Sentiment: No sentiment recognized! \n\n")
        for tone in tweet['sentiment']['document_tone']['tones']:
            print("Sentiment: {0}; Score: {1} \n\n".format(tone['tone_name'], tone['score']))
    return(tweets)


# In[5]:


def analyseTweets(tweets):
    tones = []
    for tweet in tweets:
        tones.append(tweet['sentiment']['document_tone']['tones'])
    toneNames = set({})
    aggregateSentiments = {}
    print("Tones found: ")
    for tone in tones:
        for item in tone:
            toneNames.add(item['tone_name'])
    for tone in tones:
        for item in tone:
            if(item['tone_name'] not in aggregateSentiments.keys()):
                print(item['tone_name'])
                aggregateSentiments.setdefault(item['tone_name'],[]).append(item['score'])
            else:
                aggregateSentiments[item['tone_name']].append(item['score'])
    for key in aggregateSentiments.keys():
        aggregateSentiments[key] = np.mean(np.array(aggregateSentiments[key]))
    df = pd.DataFrame(aggregateSentiments, index=['values'])
    df = df.transpose()
    maxSentiment = df.where(df['values'] == df['values'].max()).dropna()
    minSentiment = df.where(df['values'] == df['values'].min()).dropna()
    print("Min sentiment: {}; Average Score: {}".format(minSentiment.index[0], minSentiment['values'][minSentiment.index[0]]))
    print("Top sentiment: {}; Average Score: {}".format(maxSentiment.index[0], maxSentiment['values'][maxSentiment.index[0]]))


# In[ ]:


tweets = getTweets(getCreds())
analyseTweets(tweets)

