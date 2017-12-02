from turtle import *
import time


#Se abre el archivo en forma de lectura y se lo asigna en una variable
archivo = open("cuadrado_3_0001.gcode", "r")

#CONSTANTES
pasosMX = 0.41667
pasosMY = 0.11764

motorActualX = 0
motorActualY = 0

XD = 0
YD = 0
DirMX = 0
DirMY = 0

pasosx = 0
pasosy = 0

pm1 = 0
pm2 = 0
b = 0
a = 0

simMovX = 0 #Mov de X en simulacion
simMovY = 0 #Mov de Y en simulacion
simMovX0 = 0
simMovY0 = 0

contY = 0
contX = 0
contXG3 = 0
contYG3 = 0

varG01 = ''

#Funcion que suma si hay coma en el array del numero
def convertir_num_decimal_string(numero):
	tamano = len(numero)
	cont = 0
	while cont < tamano and numero[cont] != ".":	#Mientras no llegue al final, debe buscar la coma
		cont += 1

	if cont == tamano:	#Veo, si son iguales, no hay coma
		return numero
	else:
		jojo = int(numero[0:cont])+1
		return str(jojo)


#Se recorre el archivo
for renglon in archivo:
	#INICIAL EL PLANO DE DIBUJO
	setup(900, 800, 0, 0)
	speed(2)
	screensize(2600, 2000)




	palabras = renglon.split(' ') #Se vectoriza todo el archivo en partes

	#SI ENCUENTRA G02 Y G03 LOS CAMBIA POR G01
	if palabras[0] == 'G02':
		palabras[0] = palabras[0].replace("G02", "G01")
	elif palabras[0] == 'G03':
		palabras[0] = palabras[0].replace("G03", "G01")

	#COMPRUEBA PUNTOS INICIALES
	if palabras[0] == 'G00':
		if palabras[1][0] == 'Z' and palabras[1][1] == '-':
			cuchilla = 1
		else:
			cuchilla_1 = 2
		#COMPRUEBA X y Y
		if palabras[1][0] == 'X' and palabras[2][0] == 'Y':
			movX0 = palabras[1].replace("X", "")
			movY0 = palabras[2].replace("Y", "")

			motorActualX = float(movX0)
			motorActualY = float(movY0)





	elif palabras[0] == 'G01':
		if palabras[1][0] == 'X' and palabras[2][0] == 'Y':
			movX1 = palabras[1].replace("X", "")
			movY1 = palabras[2].replace("Y", "")


			if float(movX1) != motorActualX:
				XD = float(movX1) - motorActualX
				simMovX = float(movX1)

			if float(movY1) != motorActualY:
				YD = float(movY1) - motorActualY
				simMovY = float(movY1)



			if XD > 0:
				DirMX = 0
				#pmX = 1
			else:
				DirMX = 1
				#pmX = 0
			if YD > 0:
				DirMY = 0
			else:
				DirMY = 1

			pasosStrX = convertir_num_decimal_string(str(XD/pasosMX))
			pasosx = int(pasosStrX)
			if pasosx < 0:
				pasosx = pasosx * -1

			pasosStrY = convertir_num_decimal_string(str(YD/pasosMY))
			pasosy = int(pasosStrY)

			if pasosy < 0:
				pasosy *= -1
			print "PASOS X: "+str(pasosx)+"PASOS Y: "+str(pasosy)

			motorActualX = float(movX1)
			motorActualY = float(movY1)



			#COMPROBACION PARA SECUENCIA DE MOVIMIENTOS
			if pasosy > 0 or pasosx > 0:
				contX = 0
				contY = 0
				print "G000001"
				#MOVIMIENTO DE AMBOS MOTORES, X SUPERA A Y
				if pasosx > pasosy and pasosy > 1:
					print "MOTOR X SUPERA A MOTOR Y"
					while contX < (pasosx + 1):
						intYaux = convertir_num_decimal_string(str(pasosy/pasosx))
						intY = int(intYaux)
						pm1 = 1
						if contX == intY: #SE VERIFICA LA INTERSECCION PARA MOVIMIENTO DE MOTOR Y
							pm2 = 1
							contX = 0
							print "INTERSECCION EN MOTOR X"
						else:
							pm2 = 0
							print "NO HAY INTERSECCION EN MOTOR X"

						if pm2 == 1:
							print "MOVIMIENTO EN MOTOR X > Y"
							goto(simMovX*10, simMovY*10)

						contX = contX + 1

						pass
				else:
					#Y SUPERA A X
					if pasosy > pasosx and pasosx > 1:
						print "MOTOR Y SUPERA A MOTOR X"
						while contY < (pasosy + 1):
							intXaux = convertir_num_decimal_string(str(pasosx/pasosy))
							intX = int(intXaux)
							pm2 = 1
							if contY == intX: #SE VERIFICA LA INTERSECCION PARA MOVIMIENTO DE MOTOR X
								pm1 = 1
								contY = 0
								print "INTERSECCION EN MOTOR Y"
							else:
								pm1 = 0
								print "NO HAY INTERSECCION EN MOTOR Y"

							if pm1 == 1:
								print "MOVIMIENTO EN MOTOR Y > X"
								goto(simMovX*10, simMovY*10)
							contY = contY + 1
					else:
						#MOVIMIENTO DE AMBOS MOTORES A PAR
						if pasosx == pasosy and pasosx > 1 and pasosy > 1:
							print "AMBOS MOTORES A LA PAR"
							goto(simMovX*10, simMovY*10)
						else:
							#MOVIMIENTO SOLO DE MOTOR X
							if pasosx > 1 and (pasosy >= 0 and pasosy <= 1):
								print "MOVIMIENTO DE X"
								pm1 = 1
								pm2 = 0
								if DirMX == 1:
									print "DIRECCION MOTOR X: 1"
									goto(simMovX*10, simMovY*10)
								else:
									print "DIRECCION MOTOR X: 0"
									goto(simMovX*10, simMovY*10)
							else:
								#MOVIMIENTO SOLO DE MOTOR Y
								if pasosy > 1 and (pasosx >= 0 and pasosx <=1):
									print "MOVIMIENTO DE Y"
									pm1 = 0
									pm2 = 1
									if DirMY == 1:
										print "DIRECCION MOTOR Y: 1"
										goto(simMovX*10, simMovY*10)
									else:
										print "DIRECCION MOTOR Y: 0"
										goto(simMovX*10, simMovY*10)










mainloop()
archivo.close()
