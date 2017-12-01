//============= MBCORP
//=== Funciones para Leer el ultrasonico srf04 
//=== con la placa de entrenamiento 
//=== Matias Leonardo Baez

/*

unsigned int d;
//Configuracion de Puertos como entradas o salidas
void setup(void)
{
	serial_begin();
	putch('*'); //Envio un caracter por serial
	srf04Begin();
}

//Bucle infinito
void loop(void)
{
	d = srf04GetDistance();
	printf("[%d]\r\n",d);
	
}
*/

//Inicializa el sensor srf04
extern void srf04Begin(void);
//Retorna la distancia leida por el srf04
extern unsigned int srf04GetDistance(void);
