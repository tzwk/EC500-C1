import subprocess

def makeVideoFromImages():
	subprocess.call("ffmpeg -framerate 1 -i captured%d.jpg output.mp4", shell=True)