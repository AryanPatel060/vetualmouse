import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui
import math
#########################
wCam ,hCam = 640 ,480
pTime = 0
tipIds =  [4,8,12,16,20]
frameRx  = 100
frameRy  = 80
smoothening = 6
plocx , plocy = 0, 0 
clocx ,clocy = 0 , 0 
#########################
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector = htm.handDetector(maxHands=1)
wScr,hScr = pyautogui.size()
pyautogui.FAILSAFE = False
# print(wScr,hScr)

while True:
    # 1. Find landmark 
    sccess , img = cap.read()
    img  = detector.findHands(img)
    lmlist = detector.findPossition(img)

    # 2. Get the tip of the index fingers
    if len(lmlist)!=0 :
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]
        cv2.circle(img,(x1,y1) , 15 ,(0,0,255) , cv2.FILLED)
        cv2.circle(img,(x2,y2) , 15 ,(0,0,255) , cv2.FILLED)
        cv2.rectangle(img,(frameRx,frameRy),(wCam-frameRx, hCam-frameRy),(100,0,240),2)

    # 3. check which finger is up
        fingers  =[]
        if lmlist[tipIds[0]][1]>lmlist[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if lmlist[tipIds[id]][2]< lmlist[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)

    # 4. only index finger : moving mode
        if fingers[1]==1 and fingers[2] == 0:
        # 5. Convert Coordinates
            x3 = np.interp(x1,(frameRx,wCam-frameRx),(0,wScr))
            y3 = np.interp(y1,(frameRy,hCam-frameRy),(0,hScr))
        # 6. smoothing the values  
            clocx  = plocx + (x3  - plocx) / smoothening
            clocy  = plocy + (y3  - plocy) / smoothening
        # 7 . move the mouse
            pyautogui.moveTo(wScr-clocx, clocy)

            plocx,plocy = clocx ,clocy
        
        # 8. click with middle finger 
        if fingers[1]==1 and fingers[2] == 1:
            length = math.hypot(x2-x1 , y2-y1)
            cv2.line(img , (x1,y1), (x2,y2),(0,0,255) , 2)

            if length < 40 :
                pyautogui.click()
            


    cTime= time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS : {int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255) , 2)

    cv2.imshow("Image",img)
    cv2.waitKey(1)