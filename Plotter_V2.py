import sys
sys.path.append('C:\\Python27\\lib\\site-packages\\wx-3.0-msw')
import wx
import serial
import time

#Variables

#PROCESO PRINCIPAL
class Main(wx.Frame):
	rutaArchivo = ""
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title)
		self.Centre()
		self.InitUI()

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
		self.btn_open.Disable()
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

	def OnQuit(self, event):
		self.Close()
	#Boton CONECTAR a la maquina
	def OnConect(self, event):
		global ser
		puerto = ''
		estado = event.GetEventObject().GetValue()
		
		if estado == True:
			#Busca el puerto disponible
			for i in range(10):
				try:
					ser = serial.Serial(i)
					puerto = ser.portstr
					ser.close()
				except:
				#print('Nada')
					pass
			#---FIN---		
			#CONEXION	
			try:  
				ser = serial.Serial()
				ser.port = puerto
				ser.open()
				print(ser.isOpen())
				print('Conectado')
				event.GetEventObject().SetLabel("Desconectar")
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
				self.btn_open.Enable()
				#----FIN----
			except: #Error de conexion
				print("Error")
				pass
			#---FIN---		
		else:
			ser.close()
			self.btn_left5.Disable()
			self.btn_left10.Disable()
			self.btn_left15.Disable()
			self.btn_left20.Disable()
			self.btn_right5.Disable()
			self.btn_right10.Disable()
			self.btn_right15.Disable()
			self.btn_right20.Disable()
			self.btn_mover.Disable()
			self.btn_open.Disable()
			print(ser.isOpen())
			event.GetEventObject().SetLabel("Conectar")

	#Control de Motor
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

	def OnOpen(self, event):
		ventana = wx.Frame(None, -1, 'win.gcode')
		ventana.SetDimensions(0, 0, 200, 50)
		#Crea el FileOpen Dialog
		openFileDialog = wx.FileDialog(ventana, "Abrir archivo", "", "", "Archivos Gcodes (*.gcode)|*.gcode", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		openFileDialog.ShowModal()
		rutaArchivo = openFileDialog.GetPath()
		print rutaArchivo
		openFileDialog.Destroy()
		pass

		
	def OnMove(self, event):
		archivo = open("circulo_20.gcode", "r")
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
				
			elif palabras[0] == 'G1':
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
					

					if pasosx > 1 and (pasosy >= 0 and pasosy <= 2):
						verXY = 1
						pm1 = 1
						pm2 = 0
						pm2_dir = 0
						
						for n in range(1,pasosx+1):
							ser.write(chr(int('00000000',2)))
							time.sleep(.002)
							a = '0000'+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
							d = int(str(a), 2)
							ser.write(chr(d))
							time.sleep(.002)
						ser.write(chr(int('00000000',2)))
							
					else:
					 	if (pasosx >= 0 and pasosx <= 1) and pasosy >= 2:
					 		verXY = 0
							pm1 = 0
							pm2 = 1
							
							for j in range(1,pasosy+1):
								ser.write(chr(int('00000000',2)))
								time.sleep(.02)
								a = '000000'+str(pm2)+str(DirMY)
								b = int(str(a), 2)
								ser.write(chr(b))
								time.sleep(.02)
							ser.write(chr(int('00000000',2)))
								
						else:
							# EJE X y EJE Y IGUALES
							if pasosx == pasosy:
								print "hola"
								pm1 = 1
								pm2 = 1
								for n in range (pasosx):
									ser.write(chr(int('00000000',2)))
									time.sleep(.05)
									a1 = '0000'+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
									b1 = int(str(a1), 2)
									ser.write(chr(b1))
									time.sleep(.05)
							else:		

								#CIRCULO
								if pasosx > 0 and pasosy > 0:
									contY = 0
									contX = 0
									if pasosx > pasosy: #> 1
										
										while contX < (pasosx+1):
											intYaux = convertir_num_decimal_string(str(pasosy/pasosx))	
											intY = int(intYaux)
											pm1 = 1
											if contX == intY:
												pm2 = 1
												contX = 0
												
											else:
												pm2 = 0	
											ser.write(chr(int('00000000',2)))
											time.sleep(.008)
											a1 = '0000'+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
											b1 = int(str(a1), 2)
											ser.write(chr(b1))
											time.sleep(.008)
											contX = contX + 1
											
									elif pasosy > pasosx: #(pasosx / pasosy) > 1
										
										while contY < (pasosy+1): #(pasosy / pasosx)
											intXaux = convertir_num_decimal_string(str(pasosx/pasosy))	
											intX = int(intXaux)
											pm2 = 1
											if contY == intX:
												pm1 = 1
												contY = 0
												
											else:
												pm1 = 0	
											ser.write(chr(int('00000000',2)))
											time.sleep(.008)
											a1 = '0000'+str(pm1)+str(DirMX)+str(pm2)+str(DirMY)
											b1 = int(str(a1), 2)
											ser.write(chr(b1))
											time.sleep(.008)
											contY = contY + 1				



											
		archivo.close()							

			
			




#print cuchilla
#print cuchilla_1
	


		

	#---FIN---
#FIN PROCESO PRINCIPAL
app = wx.App()#Abre la APP
Main(None, 'Plotter V2')#Se llama al proceso principal
app.MainLoop()#Se crea el ciclo		
