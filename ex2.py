import tweepy

consumer_key =  'OX8dPTwnqRm8pR9UEvyy9lrRR'
consumer_secret = 'Qa0Wrbvf8pnqVa1JEYPnKVXAZHssCtVLMFbrPuyO28Dyq2e68e'
access_token = '920695116150525953-Uf1blZlllGja7CDAHPQrVD5ZriAZNMb'
access_token_secret =  'u0WN80vQtLhxT1JfOCd4GU7fXBTolwfxkzzyl1kxlPtF6'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print (tweet)