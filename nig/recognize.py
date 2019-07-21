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
import jsonify
import requests
detector="C:/Users/user/Desktop/nig/face_detection_model"
embedding_model="C:/Users/user/Desktop/nig/nn4.small2.v1.t7"

le="C:/Users/user/Desktop/nig/output/le.pickle"
recognizer="C:/Users/user/Desktop/nig/output/recognizer.pickle"

#embedding_model="C:/Users/user/Desktop/nig/nn4.small2.v1.t7"
embeddings="C:/Users/user/Desktop/nig/output/embeddings.pickle"
# load the face embedding
# load our serialized face detector from disk
print("[INFO] loading face detector...")

protoPath="C:/Users/user/Desktop/nig/face_detection_model/deploy.prototxt"
modelPath="C:/Users/user/Desktop/nig/face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch("C:/Users/user/Desktop/nig/openface_nn4.small2.v1.t7")

# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open("C:/Users/user/Desktop/nig/output/recognizer.pickle", "rb").read())
le = pickle.loads(open("C:/Users/user/Desktop/nig/output/le.pickle", "rb").read())

# initialize the video stream, then allow the camera sensor to warm up
print("[INFO] starting video stream...")
#vs = VideoStream(src='https://6f5b3f65.ngrok.io/camera').start()
#vs = cv2.VideoCapture("https://6f5b3f65.ngrok.io/camera")
#vs=cap.open("https://6f5b3f65.ngrok.io/camera")
#vs = VideoStream(src=0).start()

fps = FPS().start()

def TrackImages():
       
	detector="C:/Users/user/Desktop/nig/face_detection_model"
	embedding_model="C:/Users/user/Desktop/nig/nn4.small2.v1.t7"

	le="C:/Users/user/Desktop/nig/output/le.pickle"
	recognizer="C:/Users/user/Desktop/nig/output/recognizer.pickle"
	
	#embedding_model="C:/Users/user/Desktop/nig/nn4.small2.v1.t7"
	embeddings="C:/Users/user/Desktop/nig/output/embeddings.pickle"
	# load the face embedding
	# load our serialized face detector from disk
	print("[INFO] loading face detector...")

	protoPath="C:/Users/user/Desktop/nig/face_detection_model/deploy.prototxt"
	modelPath="C:/Users/user/Desktop/nig/face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

	# load our serialized face embedding model from disk
	print("[INFO] loading face recognizer...")
	embedder = cv2.dnn.readNetFromTorch("C:/Users/user/Desktop/nig/openface_nn4.small2.v1.t7")

	# load the actual face recognition model along with the label encoder
	recognizer = pickle.loads(open("C:/Users/user/Desktop/nig/output/recognizer.pickle", "rb").read())
	le = pickle.loads(open("C:/Users/user/Desktop/nig/output/le.pickle", "rb").read())

	# initialize the video stream, then allow the camera sensor to warm up
	print("[INFO] starting video stream...")
	#vs = VideoStream(src='192.168.37.1:8080').start()
	#vs=cap.open("https://6f5b3f65.ngrok.io/camera")
	#vs = VideoStream(src=0).start()
	

	# start the FPS throughput estimator
	fps = FPS().start()
	vs = cv2.VideoCapture(0)

	# loop over frames from the video file stream
	while True:
		# grab the frame from the threaded video stream
		_, frame = vs.read()
		#frame="http://192.168.43.109:8081/video"

		# resize the frame to have a width of 600 pixels (while
		# maintaining the aspect ratio), and then grab the image
		# dimensions
		nframe = imutils.resize(frame, width=600)
		(h, w) = nframe.shape[:2]

		# construct a blob from the image
		imageBlob = cv2.dnn.blobFromImage(
			cv2.resize(nframe, (300, 300)), 1.0, (300, 300),
			(104.0, 177.0, 123.0), swapRB=False, crop=False)

		# apply OpenCV's deep learning-based face detector to localize
		# faces in the input image
		detector.setInput(imageBlob)
		detections = detector.forward()

		# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the prediction
			confidence = detections[0, 0, i, 2]
			
			

			# filter out weak detections
			if confidence > 0.5 : #args["confidence"]:#low confidence value gives bery incorrect that
				#conf> 0.001 very pooor
				#conf>0   worst
				#conf>1 gives nothing as confidence cant be greater than 1
				#conf>0.999 best
				# compute the (x, y)-coordinates of the bounding box for
				# the face
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				
				(startX, startY, endX, endY) = box.astype("int")

				# extract the face ROI
				face = nframe[startY:endY, startX:endX]
				(fH, fW) = face.shape[:2]

				# ensure the face width and height are sufficiently large
				if fW < 20 or fH < 20:
					continue

				# construct a blob for the face ROI, then pass the blob
				# through our face embedding model to obtain the 128-d
				# quantification of the face
				faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
					(96, 96), (0, 0, 0), swapRB=True, crop=False)
				embedder.setInput(faceBlob)
				vec = embedder.forward()

				# perform classification to recognize the face
				preds = recognizer.predict_proba(vec)[0]
				j = np.argmax(preds)
				proba = preds[j]
				name = le.classes_[j]

				# draw the bounding box of the face along with the
				# associated probability
				text = "{}: {:.2f}%".format(name, proba * 100)
				y = startY - 10 if startY - 10 > 10 else startY + 10
				cv2.rectangle(nframe, (startX, startY), (endX, endY),
					(0, 0, 255), 2)
				cv2.putText(nframe, text, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

		
		# update the FPS counter
		fps.update()
		
		#print(text)
		# show the output frame
		cv2.imshow("Frame", nframe)
        
        
        
		requests.post("http://172.16.30.58:8080/detected", json = {"data":name}, timeout = 5)
		key = cv2.waitKey(1) & 0xFF
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

	# do a bit of cleanup
	cv2.destroyAllWindows()
	return 
TrackImages()	

#app.run(host='localhost',port=8080, debug=True)
#,debug=true)
