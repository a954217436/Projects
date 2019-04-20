# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 15:05:54 2019

@author: Sean
"""
import cv2
import datetime

url = 'rtsp://admin:XXXX@(IP)/Streaming/Channels/1'

cap = cv2.VideoCapture(url)
#cap2 = cv2.VideoCapture(url2)

if cap.isOpened()==False:
    print('Cap1 Fail!')
#if not cap2.isOpened()==False:
#    print('Cap2 Fail!')


while(cap.isOpened()):# and cap2.isOpened()):
    ret, frame = cap.read()
#    ret2, frame2 = cap2.read()
    
    cv2.imshow('frame', frame)
#    cv2.imshow('frame2', frame2)
    
    k = cv2.waitKey(20)
    if k == ord('q') :
        break
#    nowTime=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
##    if k == ord('s') or k == ord('c'):
##        cv2.imwrite('%sCap.jpg'%(nowTime), frame)
#    cv2.imwrite('%sCap.jpg'%(nowTime), frame)
cap.release()
#cap2.release()
cv2.destroyAllWindows()
