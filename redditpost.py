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
    #print("Get Sentences: " + str(sentences))
    if len(sentences[0]) < limit:
        final = final + str(sentences[0])
        #print("Final 1: "+ str(final))
        for i in range(1,(len(sentences))):
            if len(''.join([final,sentences[i]])) < int(limit) - 1:
                final = final + " " + str(sentences[i])
                #print("New final: " + final)
            else:
                break
        #print("THE FINAL: " + final)
        return final
    else:
        return getrandom()

def sentences(text, limit):
#    try:
#        unicode(text, "ascii")
#    except UnicodeError:
#        text = unicode(text, "utf-8")
#    print("DECODED: " + str(text))
    #print(limit)
    sentences = []
    m = re.split(r'(?<=[^A-Z].[.?!]) +(?=[0-9a-zA-Z])', str(text.encode('utf-8')))
    for i in m:
        sentences.append(i)
        #print(i)
    return getsentences(sentences, limit)

def tweet(tweettext,subandlink):
    body = str(tweettext).strip() + "\n" + str(subandlink)
    print(body)
    twitter.update_status(body)

def getrandom():
    global track
    number = random.randint(1,len(track))
    print(number)
    pretext = reddit.comment(id=track[number]).body
    sub = "r/" + reddit.comment(id=track[number]).subreddit.display_name
    link = "https://www.reddit.com" + str(reddit.comment(id=track[number]).permalink)
    shortlink = b.shorten(uri=link)["url"]
    print(pretext)
    #print(sub)
    #print(shortlink)
    subandlink = "(" + str(sub) + ": " + str(shortlink) + ")"
    tweettext = sentences(pretext, 280-len(subandlink))
    tweet(tweettext,subandlink)
    track = []

def main():
    global track
    global LENGTH_OF_TIME
    t_end = time.time() + (int(LENGTH_OF_TIME)*60)
    for comment in reddit.subreddit('all').stream.comments():
        #print(reddit.comment(comment).body)
        #print(comment)
        track.append(comment)
        if time.time() > t_end:
            break
    getrandom()

while True:
    main()
    time.sleep(int(HOW_OFTEN)*60)
