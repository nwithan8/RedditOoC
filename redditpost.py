#!/usr/bin/python

import praw
import random
import time
import bitly_api
import re
import tweepy

LENGTH_OF_TIME = 1
HOW_OFTEN = 15

#Bit.ly API Credentials
B_API_USER = 'xxxx'
B_API_KEY = 'xxxx'

b = bitly_api.Connection(B_API_USER,B_API_KEY)

#Reddit API Credentials
reddit = praw.Reddit(client_id='xxxx',client_secret='xxxx',user_agent='User-Agent: RedditOOC (by /u/grtgbln)')
all = reddit.subreddit('All')

#Twitter API Credentials
consumer_key = 'xxxx'
consumer_secret = 'xxxx'
access_token = 'xxxx'
access_secret = 'xxxx'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
twitter = tweepy.API(auth)

track = []

def getsentences(sentences, limit):
    final = ""
    #If the first sentence is less than the remaining space available in a tweet, start adding each sentence one at a time until the limit is reached.
    #If the first sentence is longer than the available space, start over with a different comment.
    if len(sentences[0]) < limit:
        final = final + str(sentences[0])
        for i in range(1,(len(sentences))):
            if len(''.join([final,sentences[i]])) < int(limit) - 1:
                final = final + " " + str(sentences[i])
            else:
                break
        return final
    else:
        return getrandom()

def sentences(text, limit): #Split the comment up into sentences
    sentences = []
    m = re.split(r'(?<=[^A-Z].[.?!]) +(?=[0-9a-zA-Z])', str(text.encode('utf-8')))
    for i in m:
        sentences.append(i)
    return getsentences(sentences, limit)

def tweet(tweettext,subandlink): #Send tweet with Subreddit and link to comment
    body = str(tweettext).strip() + "\n" + str(subandlink)
    print(body)
    twitter.update_status(body)

def getrandom(): #Pull a random comment from the stored list of ids
    global track
    number = random.randint(1,len(track))
    print(number)
    pretext = reddit.comment(id=track[number]).body
    sub = "r/" + reddit.comment(id=track[number]).subreddit.display_name
    link = "https://www.reddit.com" + str(reddit.comment(id=track[number]).permalink)
    shortlink = b.shorten(uri=link)["url"]
    subandlink = "(" + str(sub) + ": " + str(shortlink) + ")"
    tweettext = sentences(pretext, 280-len(subandlink))
    tweet(tweettext,subandlink)
    track = []

def main():
    global track
    global LENGTH_OF_TIME
    t_end = time.time() + (int(LENGTH_OF_TIME)*60)
    #For 1 minute, collect the ids of all new comments posted in r/All
    for comment in reddit.subreddit('all').stream.comments():
        track.append(comment)
        if time.time() > t_end:
            break
    getrandom()

while True:
    main()
    time.sleep(int(HOW_OFTEN)*60) #Run once every 15 minutes
