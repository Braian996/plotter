//============= MBCORP
//=== Funciones para control de 2 motor pap
//=== con la placa doble Driver L293D
//=== Matias Leonardo Baez

/*

//Configuracion de Puertos como entradas o salidas
void setup(void)
{
	papX2Begin(); //inicia el puerto b donde estan los 2 l293d
	papStop(); //apaga los motores
}

//Bucle infinito
void loop(void)
{
	papMoveManual(0b00001011); //hace que los dos motores den un
							   //paso en sentidos opuestos
	delay(250); //esperamos 250 ms antes de dar mas pasos.
}

*/

//inicializa el puerto b para controlar dos pap con dos l293d
extern void papX2Begin(void);
//ejecuta pasos en los dos motores por protocolo 0b0000PDPD
extern void papMove(unsigned char pActual);
//detiene los dos motores pap
extern void papStop(void);
//mueve los motores pap, usar para testear funcionamiento
extern void papMoveManual(unsigned char a);



