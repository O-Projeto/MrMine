import serial
import time

# Configurar a porta serial
esp = serial.Serial(port='COM9', baudrate=115200, timeout=.1)

def enviar_comando(x):
    esp.write(bytes(x, "utf-8"))
    # retorno = esp.readline()
    # print (retorno)
    time.sleep(0.1)  # Aguarda para dar tempo ao ESP32 para processar


def cordenadas(matriz):
    t = matriz[0][1]
    point= matriz[1][1]
    m= matriz[2][1]
    ff= matriz[3][1]
    p=matriz[4][1]
    msg = format(t, '04d')+","+ format(point, '04d')+","+ format(m, '04d')+","+ format(ff, '04d')+","+ format(p, '04d')
    print(msg)
    enviar_comando(msg)


