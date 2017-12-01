import time
import turtle

archivo = open("cuadrado2_0001.gcode", "r")
#VERIFICACION
verXY = 0
#CONSTANTES
pasosMX = 0.41667
pasosMY = 0.11764

#Variable de PASOS y DIRECCION motor
pm1 = 0
pm2 = 0

intX = 0
intY = 0

pm1_dir = 0
pm2_dir = 0


#---FIN
cuchilla = 0
cuchilla_1 = 0
movX0 = 0
movY0 = 0
movX1 = 0
movY1 = 0
XD = 0
YD = 0
motorActualX = 0
motorActualY = 0
pasosx = 0
pasosy = 0
DirMX = 0
DirMY = 0

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

#
for renglon in archivo:
	palabras = renglon.split(' ')
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

			if float(movY1) != motorActualY:
				YD = float(movY1) - motorActualY



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
			#print "PASOS X"+str(pasosx)+"PASOS Y"+str(pasosy)

			motorActualX = float(movX1)
			motorActualY = float(movY1)


			if pasosx > 1 and (pasosy >= 0 or pasosy <= 2):
				verXY = 1
				pm1 = 1
				pm2 = 0
				for n in range(1,pasosx+1):
					# ser.write(chr(int('00000000',2)))
					# time.sleep(.002)
					# a = '0000'+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
					# d = int(str(a), 2)
					# ser.write(chr(d))
					print "PASOS X: "+str(n)+" DIRECCION X: "+str(DirMX)
					time.sleep(.002)
				#ser.write(chr(int('00000000',2)))

			else:
			 	if (pasosx >= 0 and pasosx <= 1) and pasosy >= 2:
			 		verXY = 0
					pm1 = 0
					pm2 = 1
					for j in range(1,pasosy+1):
						# ser.write(chr(int('00000000',2)))
						# time.sleep(.02)
						# a = '000000'+str(pm2)+str(DirMY)
						# b = int(str(a), 2)
						# ser.write(chr(b))
						print "PASOS Y: "+str(j)+" DIRECCION Y: "+str(DirMY)
						time.sleep(.02)
					#ser.write(chr(int('00000000',2)))
				else:
					# EJE X y EJE Y IGUALES
					if pasosx == pasosy:
						print "hola"
						pm1 = 1
						pm2 = 1
						for n in range (pasosx):
							# ser.write(chr(int('00000000',2)))
							# time.sleep(.05)
							# a1 = '0000'+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
							# b1 = int(str(a1), 2)
							# ser.write(chr(b1))
							time.sleep(.05)
					else:

						#CIRCULO
						if pasosx > 0 and pasosy > 0:
							contY = 0
							contX = 0
							if pasosx/2 > pasosy/2: #> 1

								while contX < (pasosx+1)/2:
									intYaux = convertir_num_decimal_string(str(pasosy/pasosx))
									intY = int(intYaux)
									pm1 = 1
									if contX == intY:
										pm2 = 1
										contX = 0

									else:
										pm2 = 0
									# ser.write(chr(int('00000000',2)))
									# time.sleep(.008)
									# a1 = '0000'+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
									# b1 = int(str(a1), 2)
									# ser.write(chr(b1))
									time.sleep(.008)
									contX = contX + 1

							elif pasosy/2 > pasosx/2: #(pasosx / pasosy) > 1

								while contY < (pasosy+1)/2: #(pasosy / pasosx)
									intXaux = convertir_num_decimal_string(str(pasosx/pasosy))
									intX = int(intXaux)
									pm2 = 1
									if contY == intX:
										pm1 = 1
										contY = 0
										for xx in range (3):
											# ser.write(chr(int('00000000',2)))
											# time.sleep(.008)
											# a = '0000'+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
											# d = int(str(a), 2)
											# ser.write(chr(d))
											time.sleep(.008)
									else:
										pm1 = 0
									# ser.write(chr(int('00000000',2)))
									# time.sleep(.008)
									# a1 = '0000'+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
									# b1 = int(str(a1), 2)
									# ser.write(chr(b1))
									time.sleep(.008)
									contY = contY + 1













#print cuchilla
#print cuchilla_1


archivo.close()
