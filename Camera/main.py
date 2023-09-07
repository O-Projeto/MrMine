import cv2 as cv
import time
import threading
import os

import ComSerial
import HandTracking as ht

# from light import luz

# documentation
# https://google.github.io/mediapipe/solutions/hands

DEBUG = False
wCam, hCam = 640, 480

cap = cv.VideoCapture(0)

cap.set(3, wCam)
cap.set(4, hCam)

detector = ht.handDetector(detectionCon=1)

# change for dict
tipIds = [4, 8, 12, 16, 20]

matriz = []


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)


    # search hand
    if(len(lmList) != 0):    
        fingers = []
        # expeption thumb
        # right hand
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        index = lmList[tipIds[0]][0]
        dist = int(lmList[tipIds[0]][1]) - int(lmList[tipIds[0] - 1][1])
        matriz.append([index, dist])            

        # excluding thumb
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            valor1 = lmList[tipIds[id]][0]
            valor2 = int(lmList[tipIds[id]][2]) - int(lmList[tipIds[id] - 2][2])
            
            # Adicione o par de valores como uma lista à matriz
            
            matriz.append([valor1, valor2])
        
        print(matriz)
        data = threading.Thread(target=ComSerial.cordenadas(matriz))
        data.start()
        matriz = []


        number_fingers = sum(fingers)
        if DEBUG:
            print(fingers, number_fingers)

        cv.putText(img, str(number_fingers), (10, 70),
                   cv.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 3)

        
    cv.imshow("Image", img)
    if cv.waitKey(20) & 0xFF == ord('q'):
        break

# print(matriz)