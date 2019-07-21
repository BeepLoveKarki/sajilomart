from flask import Flask, render_template, Response
import cv2
import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as numpy
import os, time
import dlib
from imutils import face_utils
from imutils.face_utils import FaceAligner
from tkinter import *
import tkinter as tk
from tkinter import Message ,Text
import shutil #offers a number of high-level operations on files and collections of files.
import csv
import numpy as np
from PIL import Image, ImageTk #Python Imaging Library
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle
from imutils import paths
import face_recognition
import pickle
import argparse
import socket
import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import io
import json
from io import StringIO
import matplotlib

def train():
	#detector="C:Users/user/Desktop/nig/face_detection_model"
	embedding_model="C:Users/user/Desktop/nig/openface_nn4.small2.v1.t7"
	dataset="C:/Users/user/Desktop/nig/TrainingImage/" #dataset
	embeddings="C:Users/user/Desktop/nig/output/embeddings.pickle " #right
	le="C:Users/user/Desktop/nig/output/le.pickle"
	recognizer="C:Users/user/Desktop/nig/output/recognizer.pickle"
	# load our serialized face detector from disk
	print("[INFO] loading face detector...")
	#protoPath = os.path.sep.join(["detector", "deploy.prototxt"])
	protoPath="C:/Users/user/Desktop/nig/face_detection_model/deploy.prototxt"
	modelPath="C:/Users/user/Desktop/nig/face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)


	# load our serialized face embedding model from disk
	print("[INFO] loading face recognizer...")
	#embedder = cv2.dnn.readNetFromTorch("embedding_model")
	embedder = cv2.dnn.readNetFromTorch("C:Users/user/Desktop/nig/openface_nn4.small2.v1.t7")
	# grab the paths to the input images in our dataset
	print("[INFO] quantifying faces...")
	imagePaths = list(paths.list_images(dataset))
	# grab the paths to the input images in our dataset

	# initialize our lists of extracted facial embeddings and
	# corresponding people names
	knownEmbeddings = []
	knownNames = []
	total = 0
	for (i, imagePath) in enumerate(imagePaths):
		# extract the person name from the image path
		print("[INFO] processing image {}/{}".format(i + 1,len(imagePaths)))
		name = imagePath.split(os.path.sep)[-2]

		# load the input image and convert it from RGB (OpenCV ordering)
		# to dlib ordering (RGB)
		image = cv2.imread(imagePath)
		image = imutils.resize(image, width=600)
		(h, w) = image.shape[:2]
		

		# construct a blob from the image
		imageBlob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300),(104.0, 177.0, 123.0), swapRB=False, crop=False)

		# apply OpenCV's deep learning-based face detector to localize
		# faces in the input image
		detector.setInput(imageBlob)
		
		detections = detector.forward()
		

		# ensure at least one face was found
		if len(detections) > 0:
			# we're making the assumption that each image has only ONE
			# face, so find the bounding box with the largest probability
			i = np.argmax(detections[0, 0, :, 2])
			
			confidence = detections[0, 0, i, 2]

			# ensure that the detection with the largest probability also
			# means our minimum probability test (thus helping filter out
			# weak detections)
			if confidence > 0.99:
				# compute the (x, y)-coordinates of the bounding box for
				# the face
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# extract the face ROI and grab the ROI dimensions
				face = image[startY:endY, startX:endX]
				(fH, fW) = face.shape[:2]

				# ensure the face width and height are sufficiently large
				if fW < 20 or fH < 20:
					continue

				# construct a blob for the face ROI, then pass the blob
				# through our face embedding model to obtain the 128-d
				# quantification of the face
				faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,(96, 96), (0, 0, 0), swapRB=True, crop=False)
				embedder.setInput(faceBlob)
				vec = embedder.forward()

				# add the name of the person + corresponding face
				# embedding to their respective lists
				knownNames.append(name)
				knownEmbeddings.append(vec.flatten())
				total += 1

	# dump the facial embeddings + names to disk
	print("[INFO] serializing {} encodings...".format(total))
	data = {"C:Users/user/Desktop/nig/output/embeddings.pickle": knownEmbeddings, "names": knownNames}

	f = open("C:Users/user/Desktop/nig/output/embeddings.pickle", "wb")
	f.write(pickle.dumps(data))
	f.close()

	# for traning the images 
	print("[INFO] loading face embeddings...")

	#data = pickle.loads(open(embeddings, "rb").read())
	data = pickle.loads(open("C:Users/user/Desktop/nig/output/embeddings.pickle", "rb").read())


	# encode the labels
	print("[INFO] encoding labels...")
	le = LabelEncoder()
	labels = le.fit_transform(data["names"])


	# train the model used to accept the 128-d embeddings of the face and
	# then produce the actual face recognition
	print("[INFO] training model...")
	recognizer = SVC(C=1.0, kernel="linear", probability=True)

	recognizer.fit(data["C:Users/user/Desktop/nig/output/embeddings.pickle"], labels)
	#recognizer.fit(data[embeddings], labels)

	# write the actual face recognition model to disk
	f = open("C:Users/user/Desktop/nig/output/recognizer.pickle", "wb")
	f.write(pickle.dumps(recognizer))

	f.close()

	# write the label encoder to disk
	f = open("C:Users/user/Desktop/nig/output/le.pickle", "wb")
	f.write(pickle.dumps(le))
	print("Trained")

	f.close()
	
train()

