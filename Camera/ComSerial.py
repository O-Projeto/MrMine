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



def range_checker(range_calculo,a,b,c,d,e):

    if a < range_calculo[0][0] or a > range_calculo[0][1]:
        print("invalido a",a)
        return "invalido"
    elif b < range_calculo[1][0] or b > range_calculo[1][1]:
        print("invalido b",b)
        return "invalido"
    elif c < range_calculo[2][0] or c > range_calculo[2][1]:
        print("invalido c",c)
        return "invalido"
    elif d < range_calculo[3][0]  or d > range_calculo[3][1]:
        print("invalido d",d)
        return "invalido"
    elif e < range_calculo[4][0] or e > range_calculo[4][1]:
        print("invalido e",e)
        return "invalido"
    else:
        return "valido"

def cordenadas(matriz,range_calibrado):
    range_calculo = range_changer(range_calibrado)
    #print("ranges",range_calculo)
    checador_validade = "valido"
    #print(matriz)
    t = matriz[0][2]
    point= matriz[1][2]
    m= matriz[2][2]
    ff= matriz[3][2]
    p= matriz[4][2]
    #print("distancias",t,point,m,ff,p)
    checador_validade = range_checker(range_calculo,t,point,m,ff,p)
    if checador_validade == "invalido":
        print("mude de posicao a mao")
        return

    t = int(conversao_proporcao(range_calculo[0],t))
    point = int(conversao_proporcao(range_calculo[1],point))
    m = int(conversao_proporcao(range_calculo[2],m))
    ff = int(conversao_proporcao(range_calculo[3],ff))
    p = int(conversao_proporcao(range_calculo[4],p))
    msg = format(int(t), '03d')+","+ format(int(point), '03d')+","+ format(int(m), '03d')+","+ format(int(ff), '03d')+","+ format(int(p), '03d')
    #print(msg)
    enviar_comando(msg)


def range_changer(range_calibrado):
    global range_calculo

    range_calculo = range_calibrado
    return range_calculo

def conversao_proporcao(range_calculo,value):
    # Check if the input value is within the range -60 to 60
    if value < range_calculo[0] or value > range_calculo[1]:
        raise ValueError("Input value must be in the range -60 to 60")
    
    # Calculate the proportion using linear interpolation
    proportion = 20 + (value - range_calculo[0]) * (130 - 20) / (range_calculo[1] - range_calculo[0])
    inverted = 130 - proportion + 20
    print(proportion,"invertido",inverted)
    return inverted

