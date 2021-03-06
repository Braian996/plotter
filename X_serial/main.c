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
unsigned char input;
//Configuracion de Puertos como entradas o salidas
void setup(void)
{
	serial_begin();
	putch('*');
	papX2Begin();
	//RA3 = 1;
	
}

//Bucle infinito
void loop(void)
{
	input = getch();
	putch(input);

//	if(!!bit_test(input, 4)==1){
//		RA3 = 1;
//	}else{
//		RA3 = 0;
//	}
	papMove(input);

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
