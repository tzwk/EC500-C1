import tweepy
from tweepy import OAuthHandler
import json
import os
import wget
#import imghdr
import numpy as np
from PIL import Image
from resizeimage import resizeimage
import subprocess
 
consumer_key = 'OX8dPTwnqRm8pR9UEvyy9lrRR'
consumer_secret = 'Qa0Wrbvf8pnqVa1JEYPnKVXAZHssCtVLMFbrPuyO28Dyq2e68e'
access_token = '920695116150525953-Uf1blZlllGja7CDAHPQrVD5ZriAZNMb'
access_secret = 'u0WN80vQtLhxT1JfOCd4GU7fXBTolwfxkzzyl1kxlPtF6'
 
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
 
# Status() is the data model for a tweet
#tweepy.models.Status.first_parse = tweepy.models.Status.parse
#tweepy.models.Status.parse = parse
# User() is the data model for a user profil
#tweepy.models.User.first_parse = tweepy.models.User.parse
#tweepy.models.User.parse = parse
# You need to do it for all the models you need
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

tweets = api.home_timeline(count=200, include_rts=False,
                           exclude_replies=True)
#last_id = tweets[-1].id
 
#while (True):
#    more_tweets = api.home_timeline(count=200,
#                                include_rts=False,
#                                exclude_replies=True,
#                                max_id=last_id-1)
# There are no more tweets
#    if (len(more_tweets) == 0):
#        break
#    else:
#        last_id = more_tweets[-1].id-1
#        tweets = tweets + more_tweets

media_files = set()
for status in tweets:
    media = status.entities.get('media', [])
    if(len(media) > 0):
        media_files.add(media[0]['media_url']) # download the picture if there's a picture in that tweet
#print media_files

#import wget
#i = 0
for media_file in media_files:
    wget.download(media_file)
    #os.rename(media_file,'%s' %i)
    #i = i+1

path = '/home/bla/Documents/ec500_c1/pictures/'
i = 0
j = 0
for filename in os.listdir(path):
    if filename.endswith('.jpg'):
#        resizeimage.resize_crop(Image.open(filename),[240,240])
        with open(filename, 'r+b') as f:
            with Image.open(f) as image:
                cover = resizeimage.resize_cover(image,[2000,2000],validate=False)
                cover.save(filename,image.format)
#        filename = np.array(filename)
#        filename = np.array(filename.resize((480,480),Image.ANTIALIAS))
##        os.rename(os.path.join(path,filename), os.path.join(path,'captured'+str(i)+'.jpg'))
        os.rename(filename,'captured'+str(i)+'.jpg')
        i = i+1
    elif filename.endswith('.png'):
#        resizeimage.resize_crop(Image.open(filename),[240,240])
        with open(filename, 'r+b') as f:
            with Image.open(f) as image:
                cover = resizeimage.resize_cover(image,[2000,2000],validate=False)
                cover.save(filename,image.format)
#        with Image.open(filename) as image:
#            filename = resizeimage.resize_fcrop(image,[240,240])
#        filename = np.array(filename)
#        filename = np.array(filename.resize((480,480),Image.ANTIALIAS))
##        os.rename(os.path.join(path,filename), os.path.join(path,'captured'+str(i)+'.png'))
        os.rename(filename,'captured'+str(j)+'.png')
        j = j +1

subprocess.call("ffmpeg -framerate 1 -i captured%d.jpg output.mp4", shell=True) 
