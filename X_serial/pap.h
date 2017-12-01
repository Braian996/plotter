//============= MBCORP
//=== Funciones para control de 1 motor pap
//=== con la placa de entrenamiento Driver L293D
//=== Matias Leonardo Baez

/*

#define PXR	200 //pasos por vuelta 360°
#define IZQ 0	//Izquierda
#define DER 1	//Derecha

unsigned char pasos;
unsigned char sentido;

//Configuracion de Puertos como entradas o salidas
void setup(void)
{
	pap_begin(); //iniciamos el puerto del pap
	pap_led_test(); //activas la depuracion con leds
	pap_stop(); //apago el motor

	pasos=0; //pasos a 0
	sentido=IZQ; // sentido de giro IZQUIERDO
}

//Bucle infinito
void loop(void)
{
	if (pasos==PXR){ //Si el motor dio una vuelta completa 360°
		pasos=0; //reinicio
		sentido=!sentido; //cambio el sentido de giro
	}
	
	pasos++; //cuento 1 paso

	if (sentido==IZQ) // si el sentido es IZQUIERDO
		pap_left(); // damos un paso a la izquierda
	else // sino el sentido es DERECHO
		pap_right(); //damos un paso a la derecha

	delay(250); //Retardo de 250Ms entre cada paso
}

*/

//inicia el puerto b donde esta el driver l293d para usar un pap
extern void pap_begin(void);
//detiene el motor pap
extern void pap_stop(void);
//motor pap da un paso a la izquierda
extern void pap_left(void);
//motor papa da un paso a la derecha
extern void pap_right(void);
//devuelve el paso que esta ejecutando (0 al 3)
extern char pap_paso(void);
//habilita los leds para ver la secuencia del pap
extern void pap_led_test(void);
