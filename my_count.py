from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import dlib
import cv2

import zmq
#########################3
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:2000')
##########################

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# load our serialized model from disk
print("[INFO] loading model...")

prototxt = 'mobilenet_ssd/MobileNetSSD_deploy.prototxt'
model = 'mobilenet_ssd/MobileNetSSD_deploy.caffemodel'
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('videos/example_01.mp4')
# cap = cv2.VideoCapture('http://192.168.8.244:8080/stream.mjpeg')

# initialize the frame dimensions (we'll set them as soon as we read
# the first frame from the video)
W = None
H = None

# start the frames per second throughput estimator
fps = FPS().start()

total_people = 0
while True:
    ret, frame = cap.read()
    

    frame = imutils.resize(frame, width=500)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # if the frame dimensions are empty, set them
    if W is None or H is None:
        (H, W) = frame.shape[:2]

    # convert the frame to a blob and pass the blob through the
    # network and obtain the detections
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
    net.setInput(blob)
    detections = net.forward()
    total_people_frame = 0
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated
        # with the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by requiring a minimum
        # confidence
        if confidence > 0.4:
            # extract the index of the class label from the
            # detections list
            idx = int(detections[0, 0, i, 1])

            # if the class label is not a person, ignore it
            if CLASSES[idx] != "person":
                continue
            total_people_frame = total_people_frame + 1
            # compute the (x, y)-coordinates of the bounding box
            # for the object
            box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
            (startX, startY, endX, endY) = box.astype("int")


            cv2.rectangle(frame, (startX,startY), (endX,endY), (0,255,0), 2)
            cv2.putText(frame, f'person {i}', (startX,startY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

    if total_people_frame != 0:
        total_people = (total_people + total_people_frame*4)/5
    print(total_people)
    socket.send_pyobj({"Total_People":round(total_people)})
    if total_people > 0:
        total_people = total_people - 0.01
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) == 27:
        exit(0)