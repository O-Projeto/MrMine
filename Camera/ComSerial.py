import serial
import time

# Configurar a porta serial
esp = serial.Serial(port='COM9', baudrate=115200, timeout=.1)
esp.flush()

def enviar_comando(x):
    esp.write(bytes(x, "utf-8"))
    # retorno = esp.readline()
    # print (retorno)
    time.sleep(0.1)  # Aguarda para dar tempo ao ESP32 para processar
    if esp.in_waiting> 0:
        line = esp.readline().decode('utf-8').rstrip()
        print(f'Received from ESP32: {line}')



def range_checker(a,b,c,d,e):
    if a < -60 or a > 60:
        print("invalido",value)
        return "invalido"
    elif b < -60 or b > 60:
        print("invalido",b)
        return "invalido"
    elif c < -60 or c > 60:
        print("invalido",c)
        return "invalido"
    elif d < -60 or d > 60:
        print("invalido",d)
        return "invalido"
    elif e < -60 or e > 60:
        print("invalido",e)
        return "invalido"
    else:
        return "valido"

def cordenadas(matriz):
    checador_validade = "valido"
    #print(matriz)
    t = matriz[0][1]
    point= matriz[1][1]
    m= matriz[2][1]
    ff= matriz[3][1]
    p= matriz[4][1]
    
    #checador_validade = range_checker(t,point,m,ff,p)
    #if checador_validade == "invalido":
    #    print("mude de posição a mão")
    #    return

    #t = int(conversao_proporcao(t))
    #point = int(conversao_proporcao(point))
    #m = int(conversao_proporcao(m))
    #ff = int(conversao_proporcao(ff))
    #p = int(conversao_proporcao(p))
    msg = format(int(t), '04d')+","+ format(int(point), '04d')+","+ format(int(m), '04d')+","+ format(int(ff), '04d')+","+ format(int(p), '04d')
    #print(msg)
    enviar_comando(msg)




def conversao_proporcao(value):
    # Check if the input value is within the range -60 to 60
    if value < -60 or value > 60:
        raise ValueError("Input value must be in the range -60 to 60")
    
    # Calculate the proportion using linear interpolation
    proportion = 20 + (value + 60) * (160 - 20) / 120
    
    return proportion

