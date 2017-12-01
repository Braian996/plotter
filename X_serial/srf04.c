//============= MBCORP
//=== Funciones para Leer el ultrasonico srf04 
//=== con la placa de entrenamiento 
//=== Matias Leonardo Baez

#include <pic.h>
#include "delay.h"
#include "funciones.h"
#include "srf04.h"

//== Con cristal de 4Mhz y preescaler en 1:2 el TMR0
//227 da como resultado un conteo cada 58 us
//226 da como resultado un conteo cada 59,99999 us
//225 da como resultado un conteo cada 62 us

//13/11/2017 distancia como entero sin signo timer a 236 osea 40us
//         distancia como caracter sin signo timer a 235 osea 48us
#define TMR0_init	236 //valor de inicio para TIMER0 elegir lo mas cercano a 60 us

static bit	TRIGGER @	port_bit(PORTB, 1); //redeficion de bit (DISPARO)
static bit	ECHO	@	port_bit(PORTB, 2); //redeficion de bit (ECO)

unsigned int dSrf04;	//Variable donde almaceno la distancia

//=== Interrupciones
void interrupt isr(void){ 
	if (T0IF){ //si desbordo el TIMER0
		T0IF = 0; //bajo la bandera de TIMER0
		dSrf04++; //aumento en 1 la distancia
		TMR0 = TMR0_init; //Inicializo el timer
	}
}

//=== Inicializa el TMR0 con la configuracion adecuada
void srf04Begin(void){

	TRISB = 0b00000100; //RB0 trigger = Salida
                      //RB1 echo = Entrada

	dSrf04 = 0; //reseteo la distancia
	OPTION = 0b00000000; //prescaler a 1:2
	GIE = 1; // Interrupciones habilitadas
	TMR0 = TMR0_init; //Precarga de timer 0;
}

//=== Devuelve la distancia en cm (la retorna o podes usar var distancia)
unsigned int srf04GetDistance(void){

	delay(50); //espera prudencial para medir
	TRIGGER = 1; //disparo
	DelayUs(8); //Espera
	TRIGGER = 0; //Fin de disparo
	DelayUs(8); //Espera

	while (!ECHO); //Espero a que llegue el eco

	dSrf04 = 0; //Reseteo el contador de distancia	
	TMR0 = TMR0_init; //precargo el timer0
	T0IE = 1; // Habilito interrupcion TIMER0

	while (ECHO); //Espero a que termine el eco mientras se mide la distancia

	T0IE = 0; // Deshabilito interrupcion TIMER0

	if (dSrf04<=3)//normalizacion minima
		dSrf04=3;

	if (dSrf04>=330 ) //normalizacion de distancia
		dSrf04=330;

	return dSrf04;
}
