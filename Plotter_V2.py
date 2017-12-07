# -*- coding: utf-8 -*-
import sys
sys.path.append('C:\\Python27\\lib\\site-packages\\wx-3.0-msw')
import wx #Se importa la libreria para grafico
import serial
import time

#Variables

#PROCESO PRINCIPAL GRAFICO
class Main(wx.Frame):

	#Se inicializa el grafico
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title)
		self.Centre()
		self.InitUI()

	#Se le agrega elementos al entorno
	def InitUI(self):
		#Variable de entorno
		self.panel = wx.Panel(self)
		self.sizer = wx.GridBagSizer(0, 0)
		#----FIN----
		#Barra menu
		menubar = wx.MenuBar()
		salir_OP = wx.Menu()

		salir_OP.Append(wx.ID_EXIT, '&Salir')
		self.Bind(wx.EVT_MENU, self.OnQuit)#Evento MENU
		menubar.Append(salir_OP, '&Archivo')
		self.SetMenuBar(menubar)
		#---FIN---

		#Botones, etc
		self.label_01 = wx.StaticText(self.panel, label = 'Motor Varilla')
		self.btn_left5 = wx.Button(self.panel, label='-5', size=(45,50))
		self.btn_left10 = wx.Button(self.panel, label='-10', size=(45,50))
		self.btn_left15 = wx.Button(self.panel, label='-15', size=(45,50))
		self.btn_left20 = wx.Button(self.panel, label='-20', size=(45,50))
		self.btn_right5 = wx.Button(self.panel, label='+5', size=(45,50))
		self.btn_right10 = wx.Button(self.panel, label='+10', size=(45,50))
		self.btn_right15 = wx.Button(self.panel, label='+15', size=(45,50))
		self.btn_right20 = wx.Button(self.panel, label='+20', size=(45,50))
		self.btn_conectar = wx.ToggleButton(self.panel, label='Conectar', size=(90,50))
		self.btn_mover = wx.Button(self.panel, label='Mover', size=(60, 50))
		self.btn_open = wx.Button(self.panel, label='Abrir', size=(60, 50))
		#---FIN---
		#Agregando controles al sizer
		self.sizer.Add(self.label_01, pos=(0,2),flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
		self.sizer.Add(self.btn_left5, pos=(2,1), flag=wx.ALL)
		self.sizer.Add(self.btn_left10, pos=(2,2), flag=wx.ALL)
		self.sizer.Add(self.btn_left15, pos=(2,3), flag=wx.ALL)
		self.sizer.Add(self.btn_left20, pos=(2,4), flag=wx.ALL)
		self.sizer.Add(self.btn_right5, pos=(3,1), flag=wx.ALL)
		self.sizer.Add(self.btn_right10, pos=(3,2), flag=wx.ALL)
		self.sizer.Add(self.btn_right15, pos=(3,3), flag=wx.ALL)
		self.sizer.Add(self.btn_right20, pos=(3,4), flag=wx.ALL)
		self.sizer.Add(self.btn_conectar, pos=(5,2), flag=wx.ALL)
		self.sizer.Add(self.btn_mover, pos=(6,2), flag=wx.ALL)
		self.sizer.Add(self.btn_open, pos=(6,3), flag=wx.ALL)
		#---FIN---
		#Configurando el sizer
		self.panel.SetSizerAndFit(self.sizer)
		#---FIN---
		#Deshabilitando botones de control Plotter
		self.btn_left5.Disable()
		self.btn_left10.Disable()
		self.btn_left15.Disable()
		self.btn_left20.Disable()
		self.btn_right5.Disable()
		self.btn_right10.Disable()
		self.btn_right15.Disable()
		self.btn_right20.Disable()
		self.btn_mover.Disable()
		#self.btn_open.Disable()
		#---FIN---
		#Habilitando EVENTOS
		self.panel.Bind(wx.EVT_TOGGLEBUTTON, self.OnConect, self.btn_conectar)
		self.panel.Bind(wx.EVT_BUTTON, self.OnLeft5, self.btn_left5)
		self.panel.Bind(wx.EVT_BUTTON, self.OnLeft10, self.btn_left10)
		self.panel.Bind(wx.EVT_BUTTON, self.OnLeft15, self.btn_left15)
		self.panel.Bind(wx.EVT_BUTTON, self.OnLeft20, self.btn_left20)
		self.panel.Bind(wx.EVT_BUTTON, self.OnRight5, self.btn_right5)
		self.panel.Bind(wx.EVT_BUTTON, self.OnRight10, self.btn_right10)
		self.panel.Bind(wx.EVT_BUTTON, self.OnRight15, self.btn_right15)
		self.panel.Bind(wx.EVT_BUTTON, self.OnRight20, self.btn_right20)
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
				ser.port = puerto
				ser.open() #Abre la conexion
				print(ser.isOpen()) #DEBUG
				print('Conectado') #DEBUG
				event.GetEventObject().SetLabel("Desconectar") #Se cambia el LABEL de boton
				#Habilito los botones de control Plotter
				self.btn_left5.Enable()
				self.btn_left10.Enable()
				self.btn_left15.Enable()
				self.btn_left20.Enable()
				self.btn_right5.Enable()
				self.btn_right10.Enable()
				self.btn_right15.Enable()
				self.btn_right20.Enable()
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
			self.btn_left5.Disable()
			self.btn_left10.Disable()
			self.btn_left15.Disable()
			self.btn_left20.Disable()
			self.btn_right5.Disable()
			self.btn_right10.Disable()
			self.btn_right15.Disable()
			self.btn_right20.Disable()
			self.btn_mover.Disable()
			#self.btn_open.Disable()
			#----FIN
			print(ser.isOpen()) #DEBUG
			event.GetEventObject().SetLabel("Conectar") #Se cambia el LABEL

	#Control de Motor Correa
	#Izquierda
	def OnLeft5(self, event):
		ser.write('r')
	def OnLeft10(self, event):
		ser.write('e')
	def OnLeft15(self, event):
		ser.write('w')
	def OnLeft20(self, event):
		ser.write('q')
	#Derecha
	def OnRight5(self, event):
		for n in range(86):
			ser.write(chr(int('00000000',2)))
			time.sleep(.02)
			a = '00000010'
			b = int(str(a), 2)
			ser.write(chr(b))
			time.sleep(.02)
	def OnRight10(self, event):
		ser.write('y')
	def OnRight15(self, event):
		ser.write('u')
	def OnRight20(self, event):
		ser.write('i')
	#---FIN MOTOR CORREA

	#BOTON PARA ABRIR ARCHIVO GCODE (EN PRUEBA)
	def OnOpen(self, event):
		global rutaArchivo #Se declara de forma global la variable rutaArchivo
		ventana = wx.Frame(None, -1, 'win.gcode') #Se crea la ventana
		ventana.SetDimensions(0, 0, 200, 50) #Se da las dimensiones
		#Crea el FileOpen Dialog
		openFileDialog = wx.FileDialog(ventana, "Abrir archivo", "", "", "Archivos Gcodes (*.gcode)|*.gcode", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		openFileDialog.ShowModal()
		rutaArchivo = openFileDialog.GetPath() #Asigna el path del archivo a la variable
		print rutaArchivo #DEBUG
		openFileDialog.Destroy() #Se destruye el objeto openFileDialog
		pass

	#Dibuja el archivo GCODE
	def OnMove(self, event):
		#Se abre el archivo en forma de lectura y se lo asigna en una variable
		archivo = open(rutaArchivo, "r")

		#CONSTANTES
		pasosMX = 0.41667 #Equivalente de 1 paso en motor X
		pasosMY = 0.11764 #Equivalente de 1 paso en motor Y

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
							cub_interc = convertir_num_decimal_string(str(pasosx / pasosy))
							#Se usa la funcion para corregir error de perdida de pasos
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
								cub_interc = convertir_num_decimal_string(str(pasosy / pasosx))
								#Se usa la funcion para corregir error de perdida de pasos
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
								if pasosx == pasosy and (pasosx > 1 and pasosy > 1):
									print "AMBOS MOTORES A LA PAR"
									pm1 = 1
									pm2 = 1
									for n in range (1, pasosx+1):
										ser.write(chr(int('00000000',2))) #Manda cero primero
										time.sleep(tiempo03)
										a1 = '000'+str(cuchilla)+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
										b1 = int(str(a1), 2)
										ser.write(chr(b1)) #Manda movimiento
										time.sleep(tiempo03)
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







#print cuchilla
#print cuchilla_1





	#---FIN---
#FIN PROCESO PRINCIPAL
app = wx.App()#Abre la APP
Main(None, 'Plotter V2')#Se llama al proceso principal
app.MainLoop()#Se crea el ciclo
