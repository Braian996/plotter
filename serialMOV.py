# -*- coding: utf-8 -*-
__author__ = "Braian Alejandro Ledesma"
__copyright__ = "Copyright 2017, Proyecto Cutting Plotter"
__version__ = "1.0"
__maintainer__ = "Braian Alejandro Ledesma"

#Modúlo de secuencia de pasos por serial
'''
Funcion de MOVIMIENTO
cant_Pasos es la cantidad cual se mueve
tim es el tiempo de espera para enviar por serial
moX y moY es el movimiento de motor, si moX-moY es 1 se mueve el motor, si es
0 no hay habilitacion de movimiento
DirX y DirY es la direccion en la cual se movera el motor
ser es el objeto serial de Plotter_V3.py y time es el import time
'''

def fPasos(cant_Pasos, tim, moX, DirX, moY, DirY, ser, time):
    for f in range(1,cant_Pasos+1): #Se hace el ciclo de movimiento
        ser.write(chr(int(str('00000000'),2))) #Se le envia 0 al plotter
        time.sleep(tim) #Se pone tiempo de espera
        h = '0000'+str(moX)+str(DirX)+str(moY)+str(DirY) #Se crea los 8 bit
        j = int(str(h),2) #Se los pasa a int elevado a 2
        ser.write(chr(j)) #Se lo envia en formato char
        time.sleep(tim)	#Se pone tiempo de espera
    return 1
