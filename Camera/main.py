import cv2 as cv
import time
import threading
import os

import keyboard

import ComSerial
import HandTracking as ht
import numpy as np
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

#tecla para calibrar
trigger_key = "c"


angulos_base = None

matriz = []



def forma_velha_calculo():
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

def compare_distances(data):
    global angulos_base
    
    # Convert the input list to a NumPy array for easier manipulation
    data_array = np.array(data)
    
    # Extract IDs, x, and y coordinates into separate arrays
    ids = data_array[:, 0]
    x_coords = data_array[:, 1]
    y_coords = data_array[:, 2]
    
    # Initialize a list to store the absolute distances
    distances = []
    
    # Compare distances between IDs 2 and 4, 5 and 8, 9 and 12, 13 and 16, 17 and 20
    pairs_to_compare = [(2, 4), (5, 8), (9, 12), (13, 16), (17, 20)]
    
    for id1, id2 in pairs_to_compare:
        # Find the corresponding x and y coordinates for the given IDs
        x1, x2 = x_coords[ids == id1], x_coords[ids == id2]
        y1, y2 = y_coords[ids == id1], y_coords[ids == id2]
        
        # Calculate the absolute distance
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if angulos_base != None:
            #print(angulos_base[str(id2)])
            if id2 == 4:
                operador = dedao_define_distancia_negativa_ou_positiva(angulos_base[str(id2)],angle)
            else:
                operador = define_distancia_negativa_ou_positiva(angulos_base[str(id2)],angle)
            if operador == "negativo":
                distance = -distance
                
            #print(distance)
        #definir distancia negativa ou positiva
        
        
        
        distances.append((id2,angle, distance))
    
    return distances





def define_distancia_negativa_ou_positiva(base,angulo_atual):
    
    

    if base > 0:
        if angulo_atual >= 0:
            if abs(base - angulo_atual) <= 90:
                return "positivo"
            else:
                return "negativo"
        elif angulo_atual >= -90 and base <= 90:
            if  (base - angulo_atual) <= 90:
                return "positivo"
            else:
                return "negativo"
        elif angulo_atual >= -180 and base > 90:
            if abs((angulo_atual+360) - base) <= 90:
                return "positivo"    
            else:
                return "negativo"
        else:
            return "negativo"
    elif base < 0:
        if angulo_atual < 0:
            if abs(base - angulo_atual) <= 90:
                return "positivo"
            else:
                return "negativo"
        elif angulo_atual < 90 and base > -90:
            if (angulo_atual - base) <= 90:
                return "positivo"
            else:
                return "negativo"
        elif angulo_atual > 90 and base >= -180:
            if abs((base+360) - angulo_atual) <= 90:
                return "positivo"
            else:
                return "falso"
        else:
            return "negativo"
    else:
        return "negativo"

def dedao_define_distancia_negativa_ou_positiva(base,angulo_atual):
    
    

    if base > 0:
        if angulo_atual >= 0:
            if abs(base - angulo_atual) <= 45:
                return "positivo"
            else:
                return "negativo"
        elif angulo_atual >= -90 and base <= 90:
            if  (base - angulo_atual) <= 45:
                return "positivo"
            else:
                return "negativo"
        elif angulo_atual >= -180 and base > 90:
            if abs((angulo_atual+360) - base) <= 45:
                return "positivo"    
            else:
                return "negativo"
        else:
            return "negativo"
    elif base < 0:
        if angulo_atual < 0:
            if abs(base - angulo_atual) <= 45:
                return "positivo"
            else:
                return "negativo"
        elif angulo_atual < 90 and base > -90:
            if (angulo_atual - base) <= 45:
                return "positivo"
            else:
                return "negativo"
        elif angulo_atual > 90 and base >= -180:
            if abs((base+360) - angulo_atual) <= 45:
                return "positivo"
            else:
                return "falso"
        else:
            return "negativo"
    else:
        return "negativo"


def key_pressed():
    global angulos_base
    print("Comecando calibracao:")
    time.sleep(0.1)
    print("Fique com a mao aberta e parada")
    time.sleep(2)
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    if(len(lmList) != 0):
        distances = compare_distances(lmList)
        angulos_base = {"4":distances[0][1],"8":distances[1][1],"12":distances[2][1],"16":distances[3][1],"20":distances[4][1]}
        print(angulos_base)
    else:
        print("mao nao detectada, aperte a tecla novamente")

#configuração inicial necessaria
print("configuracao inicial")
time.sleep(3)
key_pressed()


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if keyboard.is_pressed(trigger_key):
        key_pressed()
        
    simbolo = "nenhum"
    # search hand
    if(len(lmList) != 0):    
        #lmList_numpy = np.array(lmList)
        #print(lmList_numpy)
        distances = compare_distances(lmList)
        #print("1", distances[0][2], "2", distances[1][2], "3" ,  distances[2][2] , "4" , distances[3][2] , "5" ,  distances[4][2])
        if distances[0][1] < 0 and distances[1][2] > 0 and distances[2][2] > 0 and distances[3][2] < 0 and distances[4][2] < 0:
            simbolo = "dois"
        elif distances[0][2] < 0 and distances[1][2] > 0 and distances[2][2] < 0 and distances[3][2] < 0 and distances[4][2] < 0:
            simbolo = "um"
        elif distances[0][2] < 0 and distances[1][2] > 0 and distances[2][2] > 0 and distances[3][2] > 0 and distances[4][2] < 0:
            simbolo = "tres"
        elif distances[0][2] > 0 and distances[1][2] > 0 and distances[2][2] > 0 and distances[3][2] < 0 and distances[4][2] < 0:
            simbolo = "tres"
        elif distances[0][2] < 0 and distances[1][2] > 0 and distances[2][2] > 0 and distances[3][2] > 0 and distances[4][2] > 0:
            simbolo = "quatro"
        elif distances[0][2] > 0 and distances[1][2] > 0 and distances[2][2] > 0 and distances[3][2] > 0 and distances[4][2] < 0:
            simbolo = "quatro"
        #elif distances[1][2] > 0 and distances[2][2] < 0 and distances[3][2] < 0 and distances[4][2] > 0:
        #    simbolo = "rock"
        elif distances[0][2] > 0 and distances[1][2] < 0 and distances[2][2] < 0 and distances[3][2] < 0 and distances[4][2] < 0:
            simbolo = "blz"
        elif distances[0][2] > 0 and distances[1][2] < 0 and distances[2][2] < 0 and distances[3][2] < 0 and distances[4][2] > 0:
            simbolo = "deboa"
        #print(matriz)
        data = threading.Thread(target=ComSerial.cordenadas(distances))
        data.start()
        matriz = []


        number_fingers = 5
        if DEBUG:
            print(fingers, number_fingers)

        cv.putText(img, str(simbolo), (100, 70),
                   cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        if lmList:
            for id, (x,y,z) in enumerate(lmList):
                cv.putText(img, str(id) + ":" + str(y) + "," + str(z) , (y + 1, z - 1), cv.FONT_HERSHEY_COMPLEX, 0.25, (0, 0, 0), 1)
        
    cv.imshow("Image", img)
    if cv.waitKey(20) & 0xFF == ord('q'):
        break

# print(matriz)