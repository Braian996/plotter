//============= MBCORP
//=== PICC simil Arduino
//=== Matias Leonardo Baez


#include <stdio.h>
#include <pic.h>
#include "delay.h"	//Retardos
#include "serial.h"	//Comunicacion Serial
#include "pap.h"	//Control PAP placa de entrenamiento
#include "papL293DX2.h"	//Control 2 PAP placa doble driver
#include "hc595.h" //Control de buffers hc595
#include "srf04.h" //Deteccion con ultrasonico srf04
#include "funciones.h"	//Funciones como arduino

__CONFIG( XT & WDTDIS & UNPROTECT & PWRTEN );

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


////===============NO TOCAR lo que sigue!!!!!!!!!

void main(void){
	
	TRISA = 0b00000000;
	TRISB = 0b00000000;

	setup();

	PORTA = 0b00000000;
	PORTB = 0b00000000;

//	INTCON=0;	// purpose of disabling the interrupts.

	while(1){
		loop();
	}
}
