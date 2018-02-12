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

import boto3

import cv2 as cv

bucket='blamonpicture1'
client=boto3.client('rekognition','us-east-2')
 
consumer_key = 'OX8dPTwnqRm8pR9UEvyy9lrRR'
consumer_secret = 'Qa0Wrbvf8pnqVa1JEYPnKVXAZHssCtVLMFbrPuyO28Dyq2e68e'
access_token = '920695116150525953-Uf1blZlllGja7CDAHPQrVD5ZriAZNMb'
access_secret = 'u0WN80vQtLhxT1JfOCd4GU7fXBTolwfxkzzyl1kxlPtF6'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

tweets = api.home_timeline(count=200, include_rts=False,
                           exclude_replies=True)

media_files = set()
for status in tweets:
    media = status.entities.get('media', [])
    if(len(media) > 0):
        media_files.add(media[0]['media_url']) # download the picture if there's a picture in that tweet

for media_file in media_files:
    try:
        wget.download(media_file)
    except IOError:
        pass

path = '/home/bla/Documents/ec500_c1/pictures/'
i = 0
j = 0
for filename in os.listdir(path):
    if filename.endswith('.jpg'):
        with open(filename, 'r+b') as f:
            with Image.open(f) as image:
                cover = resizeimage.resize_cover(image,[2000,2000],validate=False)
                cover.save(filename,image.format)
        #########detecting############
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
        os.rename(filename,'captured'+str(i)+'.jpg')
        i = i+1
    elif filename.endswith('.png'):
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
        os.rename(filename,'captured'+str(j)+'.png')
        j = j +1

subprocess.call("ffmpeg -framerate 1 -i captured%d.jpg output.mp4", shell=True) 
