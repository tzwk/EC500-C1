from tweepy import *;
import wget

def authenticateTwitter(consumer_key, consumer_secret, access_token, access_secret):
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	api = tweepy.API(auth)

def getHomeTimelinePictureURLS(api, count=200, include_rts=False, exclude_replies=True):
	tweets = api.home_timeline(count, include_rts, exclude_replies)

	media_file_urls = set()
	for status in tweets:
	    media = status.entities.get('media', [])
	    if(len(media) > 0):
	        media_file_urls.add(media[0]['media_url'])

	return media_file_urls

def downloadImagesToCurrentDirectoryFromURLS(media_file_urls):
	for media_url in media_file_urls:
    try:
        wget.download(media_file)
    except IOError:
        pass