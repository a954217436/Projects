# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 16:28:48 2019

@author: Sean
"""

# 摄像头人脸检测

import cv2
import datetime

url = 'rtsp://admin:XXXX@(IP)/Streaming/Channels/1'
 
cap=cv2.VideoCapture(url)
#cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
#cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")
cascade = cv2.CascadeClassifier("haarcascade_upperbody.xml")

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(120, 200))
    if len(rects)>0:
        for rect in rects:
            x, y, w, h = rect
            cv2.rectangle(frame, (x, y), (x+w, y+h), color = (0,255,0), thickness = 2)
        nowTime=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        cv2.imwrite(u'Body%s.jpg'%nowTime, frame)
        print('Detected One!  '+nowTime)
    cv2.imshow('Video', frame)
    if cv2.waitKey(10)==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
