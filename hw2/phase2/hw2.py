import tweepy
from tweepy import OAuthHandler
import json
import os
import os.path
#import wget
import urllib.request
#import imghdr
import numpy as np
from PIL import Image
from resizeimage import resizeimage
import subprocess

import boto3

import cv2 as cv

import pymongo
from pymongo import MongoClient
import pprint

client=boto3.client('rekognition','us-east-2') #the client configuration

#the twitter account details 
consumer_key = 'mwzfDqMTCwRxBrGtJnWiBq0Ir'
consumer_secret = 'PbmHcqAHpoAF5NqT4MjdhLCKOQXdXRYt6v6IFltypENsInrGsd'
access_token = '920695116150525953-Uf1blZlllGja7CDAHPQrVD5ZriAZNMb'
access_secret = 'u0WN80vQtLhxT1JfOCd4GU7fXBTolwfxkzzyl1kxlPtF6'

#get access to my account 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

#get the first 200 tweets in my timeline, as not all the tweets have pictures, 
#we will roughly get 50 pictures.
tweets = api.home_timeline(count=200, include_rts=False,
                           exclude_replies=True)

media_files = set() #the set which contain picture urls
screennames = []###screennames
for status in tweets:
    media = status.entities.get('media', [])#get all the 'media' entities in all the tweets
    if(len(media) > 0):
        media_files.add(media[0]['media_url']) # download the picture if there's a picture in that tweet
        screennames.append(status.author._json['screen_name'])###list of screennames

h = 0
for media_file in media_files:
    try:
        #wget.download(media_file) #download pictures in the urls using wget
        urllib.request.urlretrieve(media_file,screennames[h]+'.'+os.path.splitext(media_file)[1])
        h = h+1

    except IOError:# there may be pictures that contain errors in tweet, we ignore them
        pass

#in this part, we detect all the jpg files, resize them, detect the labels, finally add labels to the pictures
path = os.getcwd()#the directory we download the pictures(which is the current directory)
i = 0 #index for numbering pictures
sup = []
for filename in os.listdir(path):
    if filename.endswith('.jpg'):
        with open(filename, 'r+b') as f: #open file in r/w binary mode
            with Image.open(f) as image:
                cover = resizeimage.resize_cover(image,[2000,2000],validate=False)# resize
                cover.save(filename,image.format)# save (because with statement will then close it)
        #########detecting############
        with open(filename,'rb') as imag: #open file in read binary mode
            response = client.detect_labels(Image={'Bytes': imag.read()})#detect objects

        ########labeling##############
        k = 1 #index for printing labels in separate lines
        img = cv.imread(filename) #use opencv to open the file
        font = cv.FONT_HERSHEY_SIMPLEX #choose font of the labeling words
        for label in response['Labels']:
        #putText(the image to display, the text to write, text start point,
        #font used, font size, text color, text thickness, type of line)
            cv.putText(img, label['Name']+':'+str(label['Confidence']), (230, 50*k), font, 2.0, (0, 255, 0), 2, cv.LINE_AA)
            k = k+1 #change line
        cv.imwrite(filename,img) #save it
        nam=filename[0]
        os.rename(filename,'captured'+str(i)+'.jpg') #rename it to make it easier to make video

        sup.append({"Screenname":nam,"Picture number":i,"labels":response['Labels']})
        

        i = i+1 #number for the next picture

    elif filename.endswith('.png'): #same code for dealing with png pictures, as there are very rarely other formats, we omit them
        with open(filename, 'r+b') as f:
            with Image.open(f) as image:
                cover = resizeimage.resize_cover(image,[2000,2000],validate=False)
                cover.save(filename,image.format)

        #########detecting############
        #response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':filename}})
        with open(filename,'rb') as imag:
            response = client.detect_labels(Image={'Bytes': imag.read()})

        ########labeling##############
        k = 1
        img = cv.imread(filename)
        font = cv.FONT_HERSHEY_SIMPLEX
        for label in response['Labels']:
            #putText(the image to display, the text to write, text start point,
            #font used, font size, text color, text thickness, type of line)
            cv.putText(img, label['Name']+':'+str(label['Confidence']), (230, 50*k), font, 2.0, (0, 255, 0), 2, cv.LINE_AA)
            k = k+1

        cv.imwrite(filename,img)
        nam=filename[0]
        os.rename(filename,'captured'+str(i)+'.png')

        sup.append({"Screenname":nam,"Picture number":i,"labels":response['Labels']})

        i = i +1
    client=boto3.client('rekognition','us-east-2') #the client configuration
    # need to be set back from mongodb client

client = MongoClient()
db = client.labels_database
collection = db.labels_collection
collection.insert_many(sup)
pprint.pprint(collection.find_one())
# make a video using ffmpeg
subprocess.call("ffmpeg -framerate 1 -i captured%d.jpg output.mp4", shell=True)

