from django.test import TestCase
from twitter_scraper import get_tweets # Importing the Twitter Scraper
from monkeylearn import MonkeyLearn # Importing the AI API
from monkeylearn.exceptions import PlanQueryLimitError
import random
##############

positive = []
negative = []
neutral = []
all = []
tokens = []

#Twitter Accounts to fetch tweets from them
twitteruser = "bobbyfinger"
token = 'ca038db0546c5f16b4dd040dcf7a7fc7f606e0a6'
data = []
c= 0
for tweet in get_tweets(twitteruser, pages=30):
    if c == 20:
        break
    data.append(tweet)
    c +=1

for tweet in data:
    try:
        ml = MonkeyLearn(token)
        result = ml.classifiers.classify(model_id = 'cl_pi3C7JiL', data=[tweet['text']])
        response = result.body
        i = response[0]
        text = i['text']
        i = i['classifications'][0]
        classf = i['tag_name']
        perc = i['confidence']*100
        perc = round(perc,1)
        if classf == 'Positive':
            lis = (text,perc)
            positive.append(lis)
        elif classf =="Neutral":
            lis = (text,perc)
            neutral.append(lis)
        elif classf =="Negative":
            lis = (text,perc)
            negative.append(lis)
        print(classf+':',str(perc)+'%')

    except PlanQueryLimitError as e:
        # No monthly queries left
        # e.response contains the MonkeyLearnResponse object
        print('token is dead')
depress = 0
positivity = 0
for tweet in data:
    likes = tweet['likes']
    if likes < 12:
        depress +=1
    elif likes > 12:
        positivity +=1


print("Positive Tweets:",len(positive))
print("Negative Tweets:",len(negative))
print("Neutral Tweets",len(neutral))
print('=============')
print("Feeling Positive:",positivity)
print("Feeling Negative:",depress)
