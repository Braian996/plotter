//============= MBCORP
//=== Funciones para la comunicacion serial 
//=== con la placa de entrenamiento 
//=== Matias Leonardo Baez


/*
//seccion de declaracion de variables
unsigned char input;

//Configuracion de Puertos como entradas o salidas
void setup(void)
{
	serial_begin();
	putch('*'); //Envio un caracter por serial
	printf("\rPresiona una tecla:\n"); //Envio por serial una cadena de caracteres
}

//Bucle infinito
void loop(void)
{
	input = getch();	//Esperamos a que llegue un caracter por serial
	printf("\rPresionaste [%c]",input);	// Escribimos por serial un msj y el caracter que leimos
}
*/

//Inicia la comunicacion serial por el puerto A
extern void serial_begin(void);
//Escribe un caracter
extern void putch(char c);
//Espera y lee un caracter
extern char getch(void);
//Espera a que llegue un caracter y lo retorna
extern char getche(void);
