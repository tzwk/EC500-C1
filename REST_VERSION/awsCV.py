import boto3
import os
import json

def createAWSClient():
	client=boto3.client('rekognition','us-east-2')

	return client

def labelAllDownloadedImages():
	listOfReponseLabels = []

	for filename in os.listdir(path):
    	if filename.endswith('.jpg'):
    		responseLabels = labelImage(filename)

    listOfReponseLabels.append(responseLabels)

def labelImage(client, filename):
	with open(filename, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image,[2000,2000],validate=False)
            cover.save(filename,image.format)
    with open(filename,'rb') as imag:
        response = client.detect_labels(Image={'Bytes': imag.read()})

    return response['Labels']