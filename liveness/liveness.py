# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 11:30:59 2019

@author: user
"""

from imutils.video import VideoStream
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os
model=""
le=""
detector=""
confidence=0.5
# load our serialized face detector from disk
print("[INFO] loading face detector...")
protoPath = os.path.sep.join(detector, "deploy.prototxt"])
modelPath = os.path.sep.join(detector,"res10_300x300_ssd_iter_140000.caffemodel"])