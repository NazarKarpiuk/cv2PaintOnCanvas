import cv2
import numpy as np


frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,frameWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,frameHeight)
cap.set(cv2.CAP_PROP_BRIGHTNESS,130)

myColors = [22,46,105,79,145,235]

myColorsValues = [255,0,255]

myPoints = []

def findColor(img,myColors,myColorsValues):
    newPoints = []
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array(myColors[0:3])
    upper = np.array(myColors[3:6])
    mask = cv2.inRange(imgHSV,lower,upper)
    x,y = getContours(mask)
    cv2.circle(imgResult,(x,y),10,myColorsValues,cv2.FILLED)
    if x!=0 and y!=0:
        newPoints.append([x,y])
#    cv2.imshow("img",mask)
    return newPoints

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
#            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x , y , w, h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(myPoints,myColorsValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorsValues, cv2.FILLED)

while True:
    success,img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img,myColors,myColorsValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorsValues)
    cv2.imshow("Result",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break