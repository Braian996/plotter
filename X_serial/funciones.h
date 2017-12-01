#include	<pic.h>

#define OUTPUT	0
#define INPUT	1

#define LOW		0
#define HIGH	1

#define ENTRADA	1
#define SALIDA	0

#define ALTO	1
#define BAJO	0

//funciones y procesos de manejo de bits
#define	port_bit(adr, bit)	((unsigned)(&adr)*8+(bit)) //reasignacion de bit a variable
#define bit_set(var,bitno) ((var) |= (1 << (bitno)))  //seteo a 1 de bit en puerto
#define bit_clr(var,bitno) ((var) &= ~(1 << (bitno))) //seteo a 0 de bit en puerto
#define bit_flip(var,bitno) ((var) ^= (1 << (bitno))) 
#define bit_test(var,bitno) ((var) & (1 << (bitno))) 

#define pinMode(var,bitno,m) if(m==OUTPUT) bit_clr(var,bitno); else bit_set(var,bitno);
#define digitalWrite(var,bitno,m) if(m==LOW) bit_clr(var,bitno); else bit_set(var,bitno);
#define digitalRead(var,bitno) !!bit_test(var,bitno)


#define pMode(bitn,state)	bitn = state
#define dWrite(bitn,state)	bitn = state
#define dRead(bitn)	bitn


static bit	S1  @	port_bit(TRISB, 0);
static bit	S2  @	port_bit(TRISB, 1);
static bit	S3  @	port_bit(TRISB, 2);
static bit	S4  @	port_bit(TRISB, 3);
static bit	S5  @	port_bit(TRISB, 4);
static bit	S6  @	port_bit(TRISB, 5);
static bit	S7  @	port_bit(TRISB, 6);
static bit	S8  @	port_bit(TRISB, 7);
static bit	S9  @	port_bit(TRISA, 0);
static bit	S10  @	port_bit(TRISA, 1);
static bit	S11  @	port_bit(TRISA, 2);
static bit	S12  @	port_bit(TRISA, 3);
static bit	S13  @	port_bit(TRISA, 4);

//====== Digital I/O

static bit	D1  @	port_bit(PORTB, 0);
static bit	D2  @	port_bit(PORTB, 1);
static bit	D3  @	port_bit(PORTB, 2);
static bit	D4  @	port_bit(PORTB, 3);
static bit	D5  @	port_bit(PORTB, 4);
static bit	D6  @	port_bit(PORTB, 5);
static bit	D7  @	port_bit(PORTB, 6);
static bit	D8  @	port_bit(PORTB, 7);
static bit	D9  @	port_bit(PORTA, 0);
static bit	D10  @	port_bit(PORTA, 1);
static bit	D11  @	port_bit(PORTA, 2);
static bit	D12  @	port_bit(PORTA, 3);
static bit	D13  @	port_bit(PORTA, 4);
