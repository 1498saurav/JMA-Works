#import shutil
import os

def removeAllFiles():
	#shutil.rmtree("/home/runner/JMA-Works/CSV")
	print("Removing Files!")
	for file in os.scandir("/home/runner/JMA-Works/CSV"):
		os.remove(file.path)
		