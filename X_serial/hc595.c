//============= MBCORP
//=== Funciones para control del hc595 
//=== con la placa de entrenamiento 
//=== Matias Leonardo Baez

#include <pic.h>
#include "delay.h"
#include "funciones.h"
#include "hc595.h"

//CONTROL 74hc595
#define	MR 0  //9 no usado + //10 pin 74hc595
#define SHCP 1  //8 //11 pin 74hc595
#define	STCP 2  //7 //12 pin 74hc595
#define	OE 3   //6  no usado -  //13 pin 74hc595
#define	DATO 4 //14 pin 74hc595

char fpa; //buffer de puerta a

void hc595Begin(void){
	TRISA = 0b00000000;
	fpa = PORTA;
}

void hc595Init(void){
	fpa=PORTA;

	bit_set(fpa,MR); 	//1
	bit_clr(fpa,SHCP); 	//0 reloj
	bit_clr(fpa,STCP); 	//0
	bit_clr(fpa,OE);	//0
	
	PORTA=fpa;
}

void hc595Data(char paquete)
{
	char i;	

	//paquete
	for (i=0; i < 8; i++)
	{
		//envio de dato
		if (bit_test(paquete,7-i))
			bit_set(fpa,DATO);
		else
			bit_clr(fpa,DATO);

		PORTA=fpa;
		delay(1);

		bit_set(fpa,SHCP); 	//1 reloj
		PORTA=fpa;
		delay(1);
		bit_clr(fpa,SHCP); 	//0 reloj
		PORTA=fpa;
	
	}
}

void hc595End(void){
	bit_set(fpa,MR); 	//1
	bit_set(fpa,STCP); 	//1 fin dato
	bit_clr(fpa,OE);	//0
	PORTA=fpa;	
}
