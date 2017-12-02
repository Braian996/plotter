from turtle import *
import time


#Se abre el archivo en forma de lectura y se lo asigna en una variable
archivo = open("circulo_20.gcode", "r")

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
	palabras = renglon.split(' ') #Se vectoriza todo el archivo en partes
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
	elif palabras[0] == 'G1':
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
			#print "PASOS X"+str(pasosx)+"PASOS Y"+str(pasosy)	

			motorActualX = float(movX1)
			motorActualY = float(movY1)

			setup(900, 800, 0, 0)
			speed(2)
			screensize(1300, 800)

			

			if pasosx >= 2 and (pasosy >= 0 and pasosy <= 1):
				print "MOTOR X SE MUEVE, MOTOR Y NO"
				if DirMX == 1:
					print "DIRECCION DE X ES 1"
					goto(simMovX*10,simMovY*10)
				else:
					print "DIRECCION DE X ES 0"
					goto(simMovX*10,simMovY*10)
					
			else:
			 	if (pasosx >= 0 and pasosx <= 1) and pasosy >= 2:
			 		print "MOTOR Y SE MUEVE, MOTOR X NO"
			 		if DirMY == 1:
			 			print "DIRECCION DE Y ES 1"
			 			goto(simMovX*10,simMovY*10)
			 			pass
			 		else:
			 			print "DIRECCION DE Y ES 0"
			 			goto(simMovX*10,simMovY*10)
			 	else:
			 				
				 	
					# EJE X y EJE Y IGUALES
					if pasosx == pasosy:
							print "MOTOR X ES IGUAL A Y"
							goto(simMovX*10,simMovY*10)
					else:		

						#CIRCULO
						if pasosx > 0 and pasosy > 0:
							contY = 0
							contX = 0
							if pasosx/2 > pasosy/2: #> 1
								print "MOTOR X ES MAYOR A MOTOR Y"
								
								while contX < (pasosx+1)/2:
									intYaux = convertir_num_decimal_string(str(pasosy/pasosx))	
									intY = int(intYaux)
									pm1 = 1
									if contX == intY:
										pm2 = 1
										contX = 0
										
									else:
										pm2 = 0	
									if pm2 == 1:
										print "INTERSECCION contX y intY"
										goto(simMovX*10, simMovY*10)
									else:
										print "NO HAY INTERSECCION contX y intY"	
									
									contX = contX + 1
									
							elif pasosy/2 > pasosx/2: #(pasosx / pasosy) > 1
								print "MOTOR Y ES MAYOR A MOTOR X"
								while contY < (pasosy+1)/2: #(pasosy / pasosx)
									intXaux = convertir_num_decimal_string(str(pasosx/pasosy))	
									intX = int(intXaux)
									pm2 = 1
									if contY == intX:
										pm1 = 1
									else:
										pm1 = 0	
									contY = contY + 1
									if pm1 == 1:
										print "INTERSECCION contY y intX"	
										goto(simMovX*10, simMovY*10)
									else:
										print "NO HAY INTERSECCION contY y intX"

										
			 		
						
			


mainloop()
archivo.close()					
