# -*- coding: utf-8 -*-
__author__ = "Ledesma Braian Alejandro, Cubilla Sebastian, Visfer David, Rodriguez Angel y Cena Emiliano"
__copyright__ = "Copyright 2017, Proyecto Cutting Plotter"
__credits__ = ["Ledesma Braian Alejandro", "Cubilla Sebastian", "Visfer David", "Rodriguez Angel", "Cena Emiliano"]
__version__ = "2.6.2"
__maintainer__ = "Ledesma Braian Alejandro y Cubilla Sebastian"
__status__ = "En produccion"

'''
 DESCRIPCION: La class Main genera la interfaz grafica y dentro de ella tiene los eventos y funciones de botones y
 la conexion serial con la plotter.
 La variable pasosMX y pasosMY es el equivalente en mm (Milimetros) de 1 paso del motor.
 la variable pm1 y pm2 deben usan los valores 0 o 1,
 0 inhabilita movimiento y 1 habilita movimiento. (pm1 - MOTOR X / pm2 - MOTOR Y)
 DirMX y DirMY usan idem valores a pm1 y pm2,
 0 cambia direccion IZQ. y 1 direccion DER.
'''


import sys
sys.path.append('C:\\Python27\\lib\\site-packages\\wx-3.0-msw')
import wx #Se importa la libreria para grafico
import serial
import time
import serialMOV #Se importa el modulo de movimiento

#Variables

#PROCESO PRINCIPAL GRAFICO
class Main(wx.Frame):

	#Se inicializa el grafico
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title)
		self.Centre() #Centra la ventana
		self.InitUI() #Llama a la funcion InitrUI

	#Se le agrega elementos al entorno
	def InitUI(self):
		#Variable de entorno
		self.panel = wx.Panel(self)
		self.sizer = wx.GridBagSizer(2, 2)
		#----FIN----
		#Barra menu
		menubar = wx.MenuBar() #Se crea el menubar
		archivo_OP = wx.Menu() #Se crea opcion Salir

		abrir_op = wx.MenuItem(archivo_OP, wx.ID_OPEN, '&Abrir\tCtrl+O') #Se crea el item abrir

		salir_OP = wx.MenuItem(archivo_OP, wx.ID_EXIT, '&Salir') #Se crea el item salir

		archivo_OP.AppendItem(abrir_op)	#Se le concatena el menuitem al menu
		archivo_OP.AppendSeparator() #Crean una linea d separacion
		archivo_OP.AppendItem(salir_OP) #Se le concatena el menuitem al menu
		self.Bind(wx.EVT_MENU, self.OnQuit, salir_OP) #Evento para cerrar archivo
		self.Bind(wx.EVT_MENU, self.OnOpen, abrir_op) #Evento para abrir archivo
		menubar.Append(archivo_OP, '&Archivo')
		self.SetMenuBar(menubar)
		#---FIN---

		#Botones, etc
		self.CajaStatic = wx.StaticBox(self.panel, label= 'MOTOR X', pos=(10,5), size=(240, 170))
		#self.label_01 = wx.StaticText(self.panel, label = 'Motor Varilla')
		#self.btnX_left5 = wx.Button(self.panel, label='-5', size=(45,50))
		self.btnX_left = wx.BitmapButton(self.panel, 1,wx.Bitmap('icons/leftArrow_24.png', wx.BITMAP_TYPE_PNG),
		style=wx.NO_BORDER, size=(45,50))
		self.btnX_left10 = wx.Button(self.panel, label='15', size=(45,50))
		self.btnX_left15 = wx.Button(self.panel, label='20', size=(45,50))
		self.btnX_left20 = wx.Button(self.panel, label='25', size=(45,50))
		#self.btnX_right5 = wx.Button(self.panel, label='+5', size=(45,50))
		self.btnX_right = wx.BitmapButton(self.panel, 2,wx.Bitmap('icons/rightArrow2_24.png', wx.BITMAP_TYPE_PNG),
		style=wx.NO_BORDER, size=(45,50))
		self.btnX_right10 = wx.Button(self.panel, label='15', size=(45,50))
		self.btnX_right15 = wx.Button(self.panel, label='20', size=(45,50))
		self.btnX_right20 = wx.Button(self.panel, label='25', size=(45,50))

		self.CajaStatic2 = wx.StaticBox(self.panel, label='MOTOR Y', pos=(260,5), size=(240, 170))
		self.btnY_left2 = wx.BitmapButton(self.panel, 1,wx.Bitmap('icons/leftArrow_24.png', wx.BITMAP_TYPE_PNG),
		style=wx.NO_BORDER, size=(45,50))
		self.btnY_left10 = wx.Button(self.panel, label='15', size=(45,50))
		self.btnY_left15 = wx.Button(self.panel, label='20', size=(45,50))
		self.btnY_left20 = wx.Button(self.panel, label='25', size=(45,50))
		self.btnY_right2 = wx.BitmapButton(self.panel, 2,wx.Bitmap('icons/rightArrow2_24.png', wx.BITMAP_TYPE_PNG),
		style=wx.NO_BORDER, size=(45,50))
		self.btnY_right10 = wx.Button(self.panel, label='15', size=(45,50))
		self.btnY_right15 = wx.Button(self.panel, label='20', size=(45,50))
		self.btnY_right20 = wx.Button(self.panel, label='25', size=(45,50))

		self.btn_conectar = wx.ToggleButton(self.panel, label='Conectar', size=(90,50))
		self.btn_mover = wx.Button(self.panel, label='Mover', size=(60, 50))
		self.btn_open = wx.BitmapButton(self.panel, -1,wx.Bitmap('icons/file_32.png', wx.BITMAP_TYPE_PNG),
		style=wx.BORDER, size=(50,50))
		#---FIN---
		#Agregando controles al sizer
		#self.sizer.Add(self.label_01, pos=(0,2),flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
		self.sizer.Add(self.btnX_left, pos=(2,2), flag=wx.ALL)
		self.sizer.Add(self.btnX_left10, pos=(2,3), flag=wx.ALL)
		self.sizer.Add(self.btnX_left15, pos=(2,4), flag=wx.ALL)
		self.sizer.Add(self.btnX_left20, pos=(2,5), flag=wx.ALL)
		self.sizer.Add(self.btnX_right, pos=(3,2), flag=wx.ALL)
		self.sizer.Add(self.btnX_right10, pos=(3,3), flag=wx.ALL)
		self.sizer.Add(self.btnX_right15, pos=(3,4), flag=wx.ALL)
		self.sizer.Add(self.btnX_right20, pos=(3,5), flag=wx.ALL)
		self.sizer.Add(self.btnY_left2, pos=(2,7), flag=wx.ALL)
		self.sizer.Add(self.btnY_left10, pos=(2,8), flag=wx.ALL)
		self.sizer.Add(self.btnY_left15, pos=(2,9), flag=wx.ALL)
		self.sizer.Add(self.btnY_left20, pos=(2,10), flag=wx.ALL)
		self.sizer.Add(self.btnY_right2, pos=(3,7), flag=wx.ALL)
		self.sizer.Add(self.btnY_right10, pos=(3,8), flag=wx.ALL)
		self.sizer.Add(self.btnY_right15, pos=(3,9), flag=wx.ALL)
		self.sizer.Add(self.btnY_right20, pos=(3,10), flag=wx.ALL)
		self.sizer.Add(self.btn_conectar, pos=(6,5), span=(1,13), flag=wx.ALL)
		self.sizer.Add(self.btn_mover, pos=(7,5), flag=wx.ALL)
		self.sizer.Add(self.btn_open, pos=(7,6), flag=wx.ALL)
		#---FIN---
		#Configurando el sizer
		self.panel.SetSizerAndFit(self.sizer)
		#---FIN---
		#Deshabilitando botones de control Plotter

		self.btnX_left10.Disable()
		self.btnX_left15.Disable()
		self.btnX_left20.Disable()

		self.btnX_right10.Disable()
		self.btnX_right15.Disable()
		self.btnX_right20.Disable()

		self.btnY_left10.Disable()
		self.btnY_left15.Disable()
		self.btnY_left20.Disable()

		self.btnY_right10.Disable()
		self.btnY_right15.Disable()
		self.btnY_right20.Disable()
		self.btn_mover.Disable()
		#self.btn_open.Disable()
		#---FIN---
		#Habilitando EVENTOS
		self.panel.Bind(wx.EVT_TOGGLEBUTTON, self.OnConect, self.btn_conectar)

		self.panel.Bind(wx.EVT_BUTTON, self.OnLeftX10, self.btnX_left10)
		self.panel.Bind(wx.EVT_BUTTON, self.OnLeftX15, self.btnX_left15)
		self.panel.Bind(wx.EVT_BUTTON, self.OnLeftX20, self.btnX_left20)

		self.panel.Bind(wx.EVT_BUTTON, self.OnRightX10, self.btnX_right10)
		self.panel.Bind(wx.EVT_BUTTON, self.OnRightX15, self.btnX_right15)
		self.panel.Bind(wx.EVT_BUTTON, self.OnRightX20, self.btnX_right20)

		self.panel.Bind(wx.EVT_BUTTON, self.OnLeftY10, self.btnY_left10)
		self.panel.Bind(wx.EVT_BUTTON, self.OnLeftY15, self.btnY_left15)
		self.panel.Bind(wx.EVT_BUTTON, self.OnLeftY20, self.btnY_left20)

		self.panel.Bind(wx.EVT_BUTTON, self.OnRightY10, self.btnY_right10)
		self.panel.Bind(wx.EVT_BUTTON, self.OnRightY15, self.btnY_right15)
		self.panel.Bind(wx.EVT_BUTTON, self.OnRightY20, self.btnY_right20)
		self.panel.Bind(wx.EVT_BUTTON, self.OnMove, self.btn_mover)
		self.panel.Bind(wx.EVT_BUTTON, self.OnOpen, self.btn_open)
		#---FIN---
		self.Show()

	#Cierra el grafico
	def OnQuit(self, event):
		self.Close()
	#Boton CONECTAR a la maquina
	def OnConect(self, event):
		global ser
		puerto = ''
		estado = event.GetEventObject().GetValue() #Obtiene el estado del boton al hacer click

		if estado == True: #Si el estado da TRUE, inicia la conexion
			#Busca el puerto disponible
			for i in range(10):
				try:
					ser = serial.Serial(i)
					puerto = ser.portstr #Se guarda el puerto disponible
					ser.close()
				except:
				#print('Nada')
					pass
			#---FIN---
			#CONEXION
			try:
				ser = serial.Serial() #Se asigna el objeto SERIAL
				ser.port = puerto #Se asigna el puerto disponible al objeto serial
				ser.open() #Abre la conexion
				print(ser.isOpen()) #DEBUG
				print('Conectado') #DEBUG
				event.GetEventObject().SetLabel("Desconectar") #Se cambia el LABEL de boton
				#Habilito los botones de control Plotter

				self.btnX_left10.Enable()
				self.btnX_left15.Enable()
				self.btnX_left20.Enable()

				self.btnX_right10.Enable()
				self.btnX_right15.Enable()
				self.btnX_right20.Enable()

				self.btnY_left10.Enable()
				self.btnY_left15.Enable()
				self.btnY_left20.Enable()

				self.btnY_right10.Enable()
				self.btnY_right15.Enable()
				self.btnY_right20.Enable()
				self.btn_mover.Enable()
				#self.btn_open.Enable()
				#----FIN----
			except: #Error de conexion
				print("Error")
				pass
			#---FIN---
		else: #Si estado da FALSE, desconecta y cierra puerto SERIAL
			ser.close()
			#DESHABILITO LOS BOTONES

			self.btnX_left10.Disable()
			self.btnX_left15.Disable()
			self.btnX_left20.Disable()

			self.btnX_right10.Disable()
			self.btnX_right15.Disable()
			self.btnX_right20.Disable()

			self.btnY_left10.Disable()
			self.btnY_left15.Disable()
			self.btnY_left20.Disable()

			self.btnY_right10.Disable()
			self.btnY_right15.Disable()
			self.btnY_right20.Disable()
			self.btn_mover.Disable()
			#self.btn_open.Disable()
			#----FIN
			print(ser.isOpen()) #DEBUG
			event.GetEventObject().SetLabel("Conectar") #Se cambia el LABEL



	#Control de Motor X
	#Izquierda MOTOR X

	def OnLeftX10(self, event):
		f = serialMOV.fPasos(15, 0.002, 1, 0, 0, 0, ser, time)
	def OnLeftX15(self, event):
		f = serialMOV.fPasos(20, 0.002, 1, 0, 0, 0, ser, time)
	def OnLeftX20(self, event):
		f = serialMOV.fPasos(25, 0.002, 1, 0, 0, 0, ser, time)
	#Derecha MOTOR X

	def OnRightX10(self, event):
		f = serialMOV.fPasos(15, 0.002, 1, 1, 0, 0, ser, time)
	def OnRightX15(self, event):
		f = serialMOV.fPasos(20, 0.002, 1, 1, 0, 0, ser, time)
	def OnRightX20(self, event):
		f = serialMOV.fPasos(25, 0.002, 1, 1, 0, 0, ser, time)
	#---FIN MOTOR X

	#Control de Motor Y
	#Izquierda MOTOR Y

	def OnLeftY10(self, event):
		f = serialMOV.fPasos(15, 0.02, 0, 0, 1, 1, ser, time)
	def OnLeftY15(self, event):
		f = serialMOV.fPasos(20, 0.02, 0, 0, 1, 1, ser, time)
	def OnLeftY20(self, event):
		f = serialMOV.fPasos(25, 0.02, 0, 0, 1, 1, ser, time)
	#Derecha MOTOR Y

	def OnRightY10(self, event):
		f = serialMOV.fPasos(15, 0.02, 0, 0, 1, 0, ser, time)
	def OnRightY15(self, event):
		f = serialMOV.fPasos(20, 0.02, 0, 0, 1, 0, ser, time)
	def OnRightY20(self, event):
		f = serialMOV.fPasos(25, 0.02, 0, 0, 1, 0, ser, time)
	#---FIN MOTOR Y

	#BOTON PARA ABRIR ARCHIVO GCODE (EN PRUEBA)
	def OnOpen(self, event):
		global rutaArchivo #Se declara de forma global la variable rutaArchivo
		ventana = wx.Frame(None, -1, 'win.gcode') #Se crea la ventana
		ventana.SetDimensions(0, 0, 200, 50) #Se da las dimensiones
		#Crea el FileOpen Dialog
		openFileDialog = wx.FileDialog(ventana, "Abrir archivo", "", "", "Archivos Gcodes (*.gcode)|*.gcode", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		openFileDialog.ShowModal() #Muestra la ventana
		rutaArchivo = openFileDialog.GetPath() #Asigna el path del archivo a la variable
		print rutaArchivo #DEBUG
		openFileDialog.Destroy() #Se destruye el objeto openFileDialog
		pass

	#Dibuja el archivo GCODE
	def OnMove(self, event):
		#Se abre el archivo en forma de lectura y se lo asigna en una variable
		archivo = open(rutaArchivo, "r")

		#CONSTANTES
		pasosMX = 0.41667 #Equivalente en mm de 1 paso en motor X
		pasosMY = 0.11764 #Equivalente en mm de 1 paso en motor Y

		#Variable de PASOS y DIRECCION motor
		pm1 = 0
		pm2 = 0
		DirMX = 0
		DirMY = 0

		#Variable de INTERSECCION
		intX = 0
		intY = 0




		cuchilla = 0 #SOLENOIDE de plotter
		#cuchilla_1 = 0 #Variables de SIMULACION

		#Variables de cant de Movimientos de GCODE
		movX0 = 0
		movY0 = 0
		movX1 = 0
		movY1 = 0

		XD = 0
		YD = 0
		#Variables auxiliares de motor
		motorActualX = 0
		motorActualY = 0

		#Pasos de maquina
		pasosx = 0
		pasosy = 0

		#Tiempo de respuesta
		tiempo01 = 0.002
		tiempo02 = 0.02
		tiempo03 = 0.05

		#Funcion que suma si hay coma en el array del numero
		def convertir_num_decimal_string(numero):
			tamano = len(numero) #Saca la cantidad de caracteres recibidos del String
			cont = 0 #Inicializa el contador
			while cont < tamano and numero[cont] != ".":	#Mientras no llegue al final, debe buscar la coma
				cont += 1

			if cont == tamano:	#Veo, si son iguales, no hay coma
				return numero
			else: #Si hay coma, elevo el numero
				jojo = int(numero[0:cont])+1
				return str(jojo)

		#Se recorre el archivo
		for renglon in archivo:

			palabras = renglon.split(' ') #Se vectoriza todo el archivo en partes

			#SI ENCUENTRA G02, G03 o G1 LOS CAMBIA POR G01
			if palabras[0] == 'G02':
				palabras[0] = palabras[0].replace("G02", "G01")
			elif palabras[0] == 'G03':
				palabras[0] = palabras[0].replace("G03", "G01")
			else:
				if palabras[0] == 'G1':
					palabras[0] = palabras[0].replace("G1", "G01")


			#COMPRUEBA PUNTOS INICIALES
			if palabras[0] == 'G00':
				if palabras[1][0] == 'Z':
					if palabras[1][1] == '-':
						cuchilla = 0
						a3 = '000'+str(cuchilla)+'0000'
						b3 = int(str(a3), 2)
						ser.write(chr(b3)) #Manda movimiento
						time.sleep(1)
					else:
						cuchilla = 1
						a3 = '000'+str(cuchilla)+'0000'
						b3 = int(str(a3), 2)
						ser.write(chr(b3)) #Manda movimiento
						time.sleep(1)
				#COMPRUEBA X y Y
				if palabras[1][0] == 'X' and palabras[2][0] == 'Y':
					movX0 = palabras[1].replace("X", "")
					movY0 = palabras[2].replace("Y", "")
					#Asigna los puntos iniciales en motorActual
					motorActualX = float(movX0)
					motorActualY = float(movY0)

			elif palabras[0] == 'G01': #COMPRUEBA MOVIMIENTO
				# if palabras[1][0] == 'Z':
				# 	if palabras[1][1] == '-':
				# 		cuchilla = 0


				#print "SOLENOIDE: "+str(cuchilla)
				#Comprueba si hay X y Y
				if palabras[1][0] == 'X' and palabras[2][0] == 'Y':
					cuchilla = 0
					#Asigna el valor de X e Y en variables para sacar pasos y distancia
					movX1 = palabras[1].replace("X", "")
					movY1 = palabras[2].replace("Y", "")

					#Comprueba el movimiento actual con el movimiento anterior para evitar repeticiones.
					#Si no hay repeticiones
					#Resta la posicion nueva con la que tiene asignado el motor actualmente
					if float(movX1) != motorActualX:
						XD = float(movX1) - motorActualX

					if float(movY1) != motorActualY:
						YD = float(movY1) - motorActualY
					#FIN


					#Al tener el valor de la cuenta anterior
					#se verificara en que direccion se debe mover el motor
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

					pasosStrX = convertir_num_decimal_string(str(XD/pasosMX)) #Se usa la funcion para corregir error de perdida de pasos
					pasosx = int(pasosStrX) #Se convierte el valor a entero
					if pasosx < 0: #Se convierte valores negativos de pasos a positivos
						pasosx = pasosx * -1

					pasosStrY = convertir_num_decimal_string(str(YD/pasosMY))
					pasosy = int(pasosStrY)

					if pasosy < 0:
						pasosy *= -1
					#print "PASOS X"+str(pasosx)+"PASOS Y"+str(pasosy)


					motorActualX = float(movX1)
					motorActualY = float(movY1)

					#COMPROBACION PARA SECUENCIA DE MOVIMIENTOS
					if pasosx > 0 or pasosy > 0:
						contX = 0
						contY = 0
						#MOVIMIENTO DE AMBOS MOTORES
						#X SUPERA A Y
						if pasosx > pasosy and pasosy > 1:
							print "MOTOR Y SUPERA A MOTOR X"
							cub_interc = convertir_num_decimal_string(str(pasosx / pasosy)) #Se saca la interseccion
							cub_int = int(cub_interc) #Se convierte el valor a entero
							xp = pasosx
							cub_cont = 0
							while(xp>0):
								xp = xp - 1
								if (cub_cont < cub_int):
									cub_cont = cub_cont + 1
									print "MOVIMIENTO SOLO EN X"
									pm1 = 1
									pm2 = 0
									ser.write(chr(int('00000000',2))) #Manda cero primero
									time.sleep(tiempo01)
									a = '000'+str(cuchilla)+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
									d = int(str(a), 2)
									ser.write(chr(d)) #Manda movimiento
									time.sleep(tiempo01)
								else:
									cub_cont = 0
									print "AMBOS MOTORES A LA PAR"
									pm1 = 1
									pm2 = 1
									ser.write(chr(int('00000000',2))) #Manda cero primero
									time.sleep(tiempo03)
									a1 = '000'+str(cuchilla)+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
									b1 = int(str(a1), 2)
									ser.write(chr(b1)) #Manda movimiento
									time.sleep(tiempo03)
						else:
							#Y SUPERA A X
							if pasosy > pasosx and pasosx > 1:
								print "MOTOR Y SUPERA A MOTOR X"
								cub_interc = convertir_num_decimal_string(str(pasosy / pasosx)) #Se saca la interseccion
								cub_int = int(cub_interc) #Se convierte el valor a entero
								yp = pasosy
								cub_cont = 0
								while(yp>0):
									yp = yp - 1
									if (cub_cont < cub_int):
										cub_cont = cub_cont + 1
										print "MOVIMIENTO SOLO EN Y"
										pm1 = 0
										pm2 = 1
										ser.write(chr(int('00000000',2))) #Manda cero primero
										time.sleep(tiempo02)
										a = '000'+str(cuchilla)+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
										d = int(str(a), 2)
										ser.write(chr(d)) #Manda movimiento
										time.sleep(tiempo02)
									else:
										cub_cont = 0
										print "AMBOS MOTORES A LA PAR"
										pm1 = 1
										pm2 = 1
										ser.write(chr(int('00000000',2))) #Manda cero primero
										time.sleep(tiempo03)
										a1 = '000'+str(cuchilla)+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
										b1 = int(str(a1), 2)
										ser.write(chr(b1)) #Manda movimiento
										time.sleep(tiempo03)
							else:
								#MOVIMIENTO DE AMBOS MOTORES A LA PAR
								if pasosx == pasosy and (pasosx > 2 and pasosy > 2):
									print "AMBOS MOTORES A LA PAR"
									pm1 = 1
									pm2 = 1
									for n in range (1, pasosx+1):
										ser.write(chr(int('00000000',2))) #Manda cero primero
										time.sleep(tiempo03)
										a1 = '000'+str(cuchilla)+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
										b1 = int(str(a1), 2)
										ser.write(chr(b1)) #Manda movimiento
										time.sleep(tiempo02)
								else:
									#MOVIMIENTO SOLO DE MOTOR X
									if pasosx > 1 and (pasosy >= 0 and pasosy <= 1):
										print "MOVIMIENTO SOLO EN X"
										pm1 = 1
										pm2 = 0
										for n in range(1,pasosx+1):
											ser.write(chr(int('00000000',2))) #Manda cero primero
											time.sleep(tiempo01)
											a = '000'+str(cuchilla)+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
											d = int(str(a), 2)
											ser.write(chr(d)) #Manda movimiento
											time.sleep(tiempo01)
										ser.write(chr(int('00000000',2)))
									else:
										#MOVIMIENTO SOLO DE MOTOR Y
										if pasosy > 1 and (pasosx >= 0 and pasosx <= 1):
											print "MOVIMIENTO SOLO EN Y"
											pm1 = 0
											pm2 = 1
											for n in range(1,pasosy+1):
												ser.write(chr(int('00000000',2))) #Manda cero primero
												time.sleep(tiempo02)
												a = '000'+str(cuchilla)+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
												d = int(str(a), 2)
												ser.write(chr(d)) #Manda movimiento
												time.sleep(tiempo02)
											ser.write(chr(int('00000000',2)))












		archivo.close() #CIERRA EL ARCHIVO DE LECTURA


	#---FIN---
#FIN PROCESO PRINCIPAL
app = wx.App()#Abre la APP
Main(None, 'Plotter V2.6')#Se llama al proceso principal
app.MainLoop()#Se crea el ciclo
