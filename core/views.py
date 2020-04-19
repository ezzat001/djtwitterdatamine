from django.shortcuts import render,redirect
from monkeylearn import MonkeyLearn # Importing the AI API
from monkeylearn.exceptions import PlanQueryLimitError
from twitter_scraper import get_tweets # Importing the Twitter Scraper
import random


def home(request):
    context = {}
    if request.method == "POST":
        data = request.POST
        user = data.get('username')
        twitter_user = user
        token = data.get('token')
        if twitter_user and not token:
            twitteruser = twitter_user

            data = []
            for tweet in get_tweets(twitteruser, pages=30):
                data.append(tweet) #text , likes replies retweets
            context['tweets'] = data
            context['author']= twitteruser

            return render(request,'tweets.html', context)
        elif token:
            twitteruser = twitter_user
            token = token
            data = []
            c= 0
            for tweet in get_tweets(twitteruser, pages=30):
                if c == 100:
                    break
                data.append(tweet)
                c +=1
            neutral = []
            positive = []
            negative = []
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
                    redirect('/deadtoken')
            depress = 0
            positivity = 0
            for tweet in data:
                likes = tweet['likes']
                if likes < 12:
                    depress +=1
                elif likes > 12:
                    positivity +=1

            positiveperc = len(positive)/len(data)
            negativeperc = len(negative)/len(data)

            context['tweets'] = data
            context['token'] = token
            depressperc = depress/len(data)
            positivityperc = positivity/len(data)
            negativeperc += depressperc*100
            positiveperc += positivityperc*100
            author = twitteruser
            context = {'author':author,'negative':negativeperc, 'positive':positiveperc}

            return render(request, 'insights.html',context)

    return render(request, 'home.html')

def deadtoken(request):

    return render(request,'insights.html')
