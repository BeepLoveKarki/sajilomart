
"""

@author: JAY KISHAN PANJIYAR
"""
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




window = tk.Tk()

window.title("Face_Recogniser")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'

 
window.geometry('1280x1280')
window.configure(background='orange')



window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

message = tk.Label(window, text="NIGRAANI" ,bg="orange"  ,fg="white"  ,width=50  ,height=3,font=('times', 30, 'italic bold ')) 

message.place(x=200, y=20)

#lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="white"  ,bg="orange" ,font=('times', 15, ' bold ') ) 
lbl.place(x=400, y=200)

txt = tk.Entry(window,width=20  ,bg="white" ,fg="black",font=('times', 15, ' bold '))
txt.place(x=700, y=215)

lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="white"  ,bg="orange"    ,height=2 ,font=('times', 15, ' bold ')) 
lbl2.place(x=400, y=300)

txt2 = tk.Entry(window,width=20  ,bg="white"  ,fg="black",font=('times', 15, ' bold ')  )
txt2.place(x=700, y=315)

lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="white"  ,bg="orange"  ,height=2 ,font=('times', 15, ' bold ')) 
lbl3.place(x=400, y=400)

message = tk.Label(window, text="" ,bg="white"  ,fg="red"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold ')) 
message.place(x=700, y=400)

lbl3 = tk.Label(window, text="Attendance : ",width=20  ,fg="white"  ,bg="orange"  ,height=2 ,font=('times', 15, ' bold  ')) 
lbl3.place(x=400, y=650)


message2 = tk.Label(window, text="" ,fg="red"   ,bg="white",activeforeground = "green",width=30  ,height=2  ,font=('times', 15, ' bold ')) 
message2.place(x=700, y=650)
 
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():  
    detector = dlib.get_frontal_face_detector()
    shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    face_aligner = FaceAligner(shape_predictor, desiredFaceWidth=200)      
    Id=(txt.get())
    name=(txt2.get())
    path="TrainingImage/"+name+Id
    nameid=path.split("/")[1]
    
    
    try:
       os.mkdir(path,777)
       
    except OSError:
        print("File cannot be created already exists")
    
    picdir="C:/Users/user/Desktop/nig/TrainingImage/"+nameid+'/'
	
    if(is_number(Id) and name.isalpha()): #for checing provided numbers are correct or not
        #cam = cv2.VideoCapture(0)
        #cam = cv2.VideoCapture('http://172.16.30.58:8090/video')
        cam=cv2.VideoCapture(0)
        clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientsocket.connect(('localhost',8089))
		
        sampleNum=0
        while(True):
            ret, img = cam.read()
 
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #faces = detector.detectMultiScale(img_gray)
            faces = detector(img_gray)
            #for (x,y,w,h) in faces:
            if len(faces) == 1:
                face=faces[0]
                
                (x, y, w, h) = face_utils.rect_to_bb(face)
                face_img = img_gray[y-50:y + h+100, x-50:x + w+100]
                face_aligned = face_aligner.align(img, img_gray, face)
                face_img = face_aligned
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                
                
                
                #cv2.imwrite(picdir+Id +'.'+ str(sampleNum) + ".jpg",gray[y:y+h,x:x+w]) #data is saved in this format
                #cv2.imwrite(picdir+Id +'.'+ str(sampleNum) + ".png",face_img)
                cv2.imwrite(picdir+'0000'+str(sampleNum) + ".jpg",face_img)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 3)
                cv2.imshow("Saving", img)
                #display the frame
                cv2.imshow('aligned',face_img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>100:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
        
	       
            writer = csv.writer(csvFile)
	    
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
    
def TrainImages():
    #extract embeddings 
	
	detector="C:/Users/user/Desktop/nig/face_detection_model"
	embedding_model="C:/Users/user/Desktop/nig/openface_nn4.small2.v1.t7"
	dataset="C:/Users/user/Desktop/nig/TrainingImage"
	embeddings="C:/Users/user/Desktop/nig/output/embeddings.pickle "
	le="C:/Users/user/Desktop/opencv-face-recognition/output/le.pickle"
	recognizer="C:/Users/user/Desktop/opencv-face-recognition/output/recognizer.pickle"
	# load our serialized face detector from disk
	print("[INFO] loading face detector...")
	#protoPath = os.path.sep.join(["detector", "deploy.prototxt"])
	protoPath="C:/Users/user/Desktop/nig/face_detection_model/deploy.prototxt"
	modelPath="C:/Users/user/Desktop/nig/face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
	#modelPath = os.path.sep.join(["detector","res10_300x300_ssd_iter_140000.caffemodel"])
	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

	# load our serialized face embedding model from disk
	print("[INFO] loading face recognizer...")
	#embedder = cv2.dnn.readNetFromTorch("embedding_model")
	embedder = cv2.dnn.readNetFromTorch(embedding_model)
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
			if confidence > 0.5:
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
	data = {"C:/Users/user/Desktop/nig/output/embeddings.pickle": knownEmbeddings, "names": knownNames}

	f = open("C:/Users/user/Desktop/nig/output/embeddings.pickle", "wb")
	f.write(pickle.dumps(data))
	f.close()
	
	# for traning the images 
	print("[INFO] loading face embeddings...")

	#data = pickle.loads(open(embeddings, "rb").read())
	data = pickle.loads(open("C:/Users/user/Desktop/nig/output/embeddings.pickle", "rb").read())


	# encode the labels
	print("[INFO] encoding labels...")
	le = LabelEncoder()
	labels = le.fit_transform(data["names"])


	# train the model used to accept the 128-d embeddings of the face and
	# then produce the actual face recognition
	print("[INFO] training model...")
	recognizer = SVC(C=1.0, kernel="linear", probability=True)

	recognizer.fit(data["C:/Users/user/Desktop/nig/output/embeddings.pickle"], labels)
	#recognizer.fit(data[embeddings], labels)

	# write the actual face recognition model to disk
	f = open("C:/Users/user/Desktop/nig/output/recognizer.pickle", "wb")
	f.write(pickle.dumps(recognizer))

	f.close()

	# write the label encoder to disk
	f = open("C:/Users/user/Desktop/nig/output/le.pickle", "wb")
	f.write(pickle.dumps(le))
	print("Trained")

	f.close()

		
	'''
    #recognizer = cv2.face_LBPHFaceRecognizer.create()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    #recognizer = cv2.createLBPHFaceRecognizer()
    harcascadePath = "C:\\Users\\user\\Desktop\\locus2019\\haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml") #also save in thi format
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)
'''
def getImagesAndLabels(path):
    #get the path of all the files in the folder
    
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]   #create empty ID list    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

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
	vs = cv2.VideoCapture("https://192.168.137.1:8080")
	#vs=cap.open("https://6f5b3f65.ngrok.io/camera")
	#vs = VideoStream(src=0).start()
	

	# start the FPS throughput estimator
	fps = FPS().start()

	# loop over frames from the video file stream
	while True:
		# grab the frame from the threaded video stream
		frame = vs.read()
		#frame="http://192.168.43.109:8081/video"

		# resize the frame to have a width of 600 pixels (while
		# maintaining the aspect ratio), and then grab the image
		# dimensions
		frame = imutils.resize(frame, width=600)
		(h, w) = frame.shape[:2]

		# construct a blob from the image
		imageBlob = cv2.dnn.blobFromImage(
			cv2.resize(frame, (300, 300)), 1.0, (300, 300),
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
				face = frame[startY:endY, startX:endX]
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
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					(0, 0, 255), 2)
				cv2.putText(frame, text, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

		# update the FPS counter
		fps.update()

		# show the output frame
		cv2.imshow("Frame", frame)
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
	vs.stop()
	'''
	recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    #harcascadePath = "C:\\Users\\user\\Desktop\\locus project\\overall final\\haarcascade_frontalface_default.xml"
    harcascadePath = "haarcascade_frontalface_default.xml"   #initially
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    #df=pd.read_csv("C:\\Users\\user\\Desktop\\locus project\\overall final\\StudentDetails\\StudentDetails.csv")
    cam = cv2.VideoCapture(1)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    #col_names =  ['Id','Name','Date','Time']
    col_names =  ['Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):  #100 is better than 200, and 0 would be a "perfect match" conf for confidence
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                #attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                attendance.loc[len(attendance)] = [date,timeStamp]
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour,Minute,Second=timeStamp.split(":")
                #fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv" effectibe one
                #fileName="Attendance\Attendance.csv"
                a=str(Id)
                fileName="IAttendance\Attendance_"+a+".csv"
                attendance.to_csv(fileName,mode='a',index=False, header=False)
                print(attendance)
                
				
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        #attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    #ts = time.time()      
    #date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    #timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    #Hour,Minute,Second=timeStamp.split(":")
    #fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    #fileName="Attendance\Attendance_.csv"
    #attendance.to_csv(fileName,index=False)
    #data=attendance
    #top=Toplevel()
    #top.geometry("500x500+300+120")
    #L=Entry(top)
    #L =Label(top,text=data).pack()
    cam.release()
    cv2.destroyAllWindows()
  '''

    
  
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="black"  ,bg="orange"  ,width=20  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="black"  ,bg="orange"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=950, y=300)    
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="white"  ,bg="black"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=200, y=500)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="white"  ,bg="black"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=500, y=500)
trackImg = tk.Button(window, text="Track Images", command=TrackImages  ,fg="white"  ,bg="black"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=800, y=500)
copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 30, 'italic bold '))#underline'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "ADMINISTRATIVE SOLUTION OF AN ORGANIZATION")#,"", "TEAM", "superscript")
copyWrite.configure(state="disabled",fg="black"  )
copyWrite.pack(side="left")
copyWrite.place(x=400, y=750)
 
window.mainloop()