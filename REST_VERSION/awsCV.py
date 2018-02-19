import boto3
import os

def createAWSClient():
	client=boto3.client('rekognition','us-east-2')

	return client

def labelAllDownloadedImages():
	listOfReponseLabels = []

	path = os.getcwd()
	for filename in os.listdir(path):
		responseLabels = labelImage(filename)

	listOfReponseLabels.append(responseLabels)

def labelImage(client, filename):
	with open(filename, 'r+b') as f:
		with Image.open(f) as image:
			cover = resizeimage.resize_cover(image,[2000,2000],validate=False)
			cover.save(filename,image.format)
	with open(filename,'rb') as imag:
		response = client.detect_labels(Image={'Bytes': imag.read()})

	saveImageAsPatternizedName(filename)

	return response['Labels']

def saveImageAsPatternizedName(filename):
	if filename.endswith('.jpg'):
		os.rename(filename,'captured'+str(i)+'.jpg')
	elif filename.endswith('.png'):
		os.rename(filename,'captured'+str(i)+'.png')