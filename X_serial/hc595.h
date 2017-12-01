//============= MBCORP
//=== Funciones para control del hc595 
//=== con la placa de entrenamiento 
//=== Matias Leonardo Baez

/*
//Configuracion de Puertos como entradas o salidas
void setup(void)
{
	hc595Begin();
}

//Bucle infinito
void loop(void)
{
	hc595Init();
	hc595Data('a');
	hc595Data(0b11111111);
	hc595End();
	delay(1);
}
*/

//Inicia el puerto A para conectar al hc595
extern void hc595Begin(void); 
//Avisa al hc595 que comenzara a recibir datos
extern void hc595Init(void);
//envia un byte al hc595
extern void hc595Data(char paquete);
//avisa al hc595 que terminamos de enviar datos
// y que ahora debe mostrarlos
extern void hc595End(void);
