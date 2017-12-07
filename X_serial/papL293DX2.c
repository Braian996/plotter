//============= MBCORP
//=== Funciones para control de 2 motor pap
//=== con la placa doble Driver L293D
//=== Matias Leonardo Baez

#include <pic.h>
#include "funciones.h"
#include "papL293DX2.h"

unsigned char sM[5]; //almacena las secuencias
unsigned char pAnterior; // secuencia en la que se encuentra
unsigned char m1Ciclo; 
unsigned char m2Ciclo;


void papX2Begin(void)
{
	TRISB = 0b00000000; //Todo el pueto B como salida

	sM[0]=0b00010000;
	sM[1]=0b00100000;
	sM[2]=0b01000000;
	sM[3]=0b10000000;
	sM[4]=0b00000000; //sin paso, para que no caliente el driver

	pAnterior=0b00000000; //
	m1Ciclo=0;
	m2Ciclo=0;
}

//0b00001111
//      PDPD   Paso Direccion
//      M1M2   Motor1 Motor2
void papMove(unsigned char pActual)
{
	//Motor1
	//si paso de estar en 0 a estar en 1
	if (!!bit_test(pActual,3)==1 && !!bit_test(pAnterior,3)==0)
	{
		if (!!bit_test(pActual,2)==1)
		{
			if (m1Ciclo==3)
				m1Ciclo=0;
			else
				m1Ciclo++;
		}
		else
		{
			if (m1Ciclo==0)
				m1Ciclo=3;
			else
				m1Ciclo--;
		}
	}

	//Motor2
	//si paso de estar en 0 a estar en 1
	if (!!bit_test(pActual,1)==1 && !!bit_test(pAnterior,1)==0)
	{
		if (!!bit_test(pActual,0)==1) //verifico la direccion
		{
			if (m2Ciclo==3)
				m2Ciclo=0;
			else
				m2Ciclo++;
		}
		else
		{
			if (m2Ciclo==0)
				m2Ciclo=3;
			else
				m2Ciclo--;
		}
	}

	if(bit_test(pActual, 4) == 1){
		//bit_set(PORTA, 3);
		RA3 = 1;
	}
	else{
		//bit_clr(PORTA, 3);
		RA3 = 0;
	} 

	PORTB = sM[m1Ciclo] | (sM[m2Ciclo]>>4); //envio al motor
	pAnterior = pActual; //lo actual ahora es lo anterior
}

void papStop(void){
	PORTB = sM[4];

	pAnterior=0b00000000; //
	m1Ciclo=0;
	m2Ciclo=0;
}

void papMoveManual(unsigned char a){
	papMove(a);
	papMove(0b00000000);
}
