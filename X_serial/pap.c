//============= MBCORP
//=== Funciones para control de 1 motor pap
//=== con la placa de entrenamiento Driver L293D
//=== Matias Leonardo Baez

#include <pic.h>
#include "funciones.h"
#include "pap.h"

unsigned char secuencia[5]; //almacena las secuencias
unsigned char Paso; // secuencia en la que se encuentra
unsigned char ld;

//inicia el control de un motor pap por el puertoB conectado a RB7-6-5-4
void pap_begin(void)
{
	TRISB &= 0b00001111;

	secuencia[0]=0b00010000;
	secuencia[1]=0b00100000;
	secuencia[2]=0b01000000;
	secuencia[3]=0b10000000;
	secuencia[4]=0b00000000; //sin Paso, para que no caliente el driver

	Paso=0; //Paso 0
	ld=0;

}

//con esta funcion no perdemos el estado de los primeros 4 bits del puerto b
char buff_pap(void){
	unsigned char temp;

	temp = PORTB << 4; //desplazo 4 posiciones hacia adelante
	temp = temp >> 4; //desplazo 4 posiciones hacia atras 
	/* Con lo anterior borro el estado de los bits del motor */
	/* Sin perder el estado de los primeros 4 bits           */

	return temp;
}

//detenemos el motor pap y evitamos que caliente el driver y su motor
void pap_stop(void){

	PORTB = secuencia[4] | buff_pap(); //genero el Paso

	if (ld==1)
		PORTA = secuencia[4] >> 4;

	Paso=0;
}

//hace que el motor haga un Paso en sentido antihorario
void pap_left(void){

	if (Paso==3)	//reiniciamos los Pasos si excedemos
		Paso=0;
	else
		Paso++;

	PORTB = secuencia[Paso] | buff_pap(); //genero el Paso
	
	if (ld==1)
		PORTA = secuencia[Paso] >> 4;
}

//hace que el motor haga un Paso en sentido horario
void pap_right(void)
{
	if (Paso==0)	//reiniciamos los Pasos si excedemos
		Paso=3;
	else
		Paso--;

	PORTB = secuencia[Paso] | buff_pap(); //genero el Paso
	
	if (ld==1)
		PORTA = secuencia[Paso] >> 4;
}

//Devuelve el Paso actual dentro la secuencia
char pap_paso(void)
{
	return Paso;
}

//hace que los leds se enciendan para testear la secuencia del pap
void pap_led_test(void)
{
	ld = 1;
}