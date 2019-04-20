# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 16:28:48 2019

@author: Sean
"""

# 运动检测 微信通知

import cv2
import datetime
import numpy as np
import itchat


def moveDetect(bg, currentImg):
    bgGray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    imgGray = cv2.cvtColor(currentImg, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(bgGray, imgGray)
    ret, thresh = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY)
    k1 = np.ones((5,5), np.uint8)
    k2 = np.ones((15,15), np.uint8)
    erode = cv2.erode(thresh, k1, iterations=3)
    dilate = cv2.dilate(erode, k2, iterations=2)
    thresh, contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cntNum = 0
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if w>50 and h>50:
            cv2.rectangle(currentImg, (x,y), (x+w,y+h), (0,255,0), 2)
            cntNum += 1
    if cntNum>0:
        cv2.putText(currentImg, 'Nums=%s'%cntNum, (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = nowTime + '.jpg'
        cv2.imwrite(filename, currentImg)
        sendMsg('Detected One Movement at '+ nowTime, filename)
#    return cntNum     
   
    
msgUnique = ''
def sendMsg(message, file):
    # nickname = input('please input your firends\' nickname : ' )
    #   想给谁发信息，先查找到这个朋友,name后填微信备注即可,deepin测试成功
    # users = itchat.search_friends(name=nickname)
    users = itchat.search_friends(name='我的小号')   # 使用备注名来查找实际用户名
    #获取好友全部信息,返回一个列表,列表内是一个字典
#    print(users)
    #获取`UserName`,用于发送消息
    userName = users[0]['UserName']
    global msgUnique
    if message != msgUnique:
        itchat.send(message, toUserName = userName)
        print('Detected Movement...')
        print('Succeed Sending...')
        msgUnique = message
        try:
            itchat.send_image(file, toUserName=userName)  #如果是其他文件可以直接send_file
            print("img sending...")
        except:
            print("img fail sending")


def logIn():
    itchat.auto_login(hotReload=True)  # 首次扫描登录后后续自动登录
    print('Login...')


def main():
    logIn()
    url = 'rtsp://admin:XXXX@(IP)/Streaming/Channels/1'
    cap=cv2.VideoCapture(url)
    if(cap.isOpened()): #视频打开成功
        flag = 1
    else:
        flag = 0
    count = 0
    if flag:
        while True:
            ret, frame = cap.read()
            if(frame is None):
                break
            count = count + 1
            if count == 1:
                bg = frame.copy()#保存第一帧图像
                continue
            else:
                moveDetect(bg, frame)
                cv2.imshow('move',frame)
            if cv2.waitKey(30) & 0xFF == 27:  #按下Esc键退出
                break
    cap.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    main()
    
