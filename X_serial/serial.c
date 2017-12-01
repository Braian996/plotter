/*
 *	Serial port driver (uses bit-banging)
 *	for 16Cxx series parts.
 *
 * 	IMPORTANT: Compile this file with FULL optimization
 *
 *	Copyright (C)1996 HI-TECH Software.
 *	Freely distributable.
 */
#include	<pic.h>
#include	"serial.h"
/*
 *	Tunable parameters
 */

/*	Transmit and Receive port bits */
#define SERIAL_PORT	PORTA
#define SERIAL_TRIS	TRISA
#define	TX_PIN		0
#define RX_PIN		1

/*	Xtal frequency */
#define	XTAL	4000000

/*	Baud rate	*/
#define	BRATE	9600

/*	Don't change anything else */
#define SCALER		10000000
#define ITIME		4*SCALER/XTAL	/* Instruction cycle time */
#if BRATE > 1200
 #define	DLY		3		/* cycles per null loop */
 #define	TX_OHEAD 13		/* overhead cycles per loop */
#else
 #define	DLY		9		/* cycles per null loop */
 #define TX_OHEAD  14
#endif
#define	RX_OHEAD	12		/* receiver overhead per loop */

#define	DELAY(ohead)	(((SCALER/BRATE)-(ohead*ITIME))/(DLY*ITIME))

static bit	TxData @ (unsigned)&SERIAL_PORT*8+TX_PIN;	/* Map TxData to pin */
static bit	RxData @ (unsigned)&SERIAL_PORT*8+RX_PIN;	/* Map RxData to pin */
#define	INIT_PORT	SERIAL_TRIS |= 1<<RX_PIN				/* set up I/O direction */

unsigned char ca;

void serial_begin(void)
{
	INIT_PORT;
}

void
putch(char c)
{
	unsigned char	bitno;
#if BRATE > 1200
	unsigned char	dly;
#else
	unsigned int	dly;
#endif

//	INIT_PORT;
	TxData = 0;			/* start bit */
	bitno = 12;
	do {
		dly = DELAY(TX_OHEAD);	/* wait one bit time */
		do
			/* waiting in delay loop */ ;
		while(--dly);
		if(c & 1)
			TxData = 1;
		if(!(c & 1))
			TxData = 0;
		c = (c >> 1) | 0x80;
	} while(--bitno);
NOP();
}

char
getch(void)
{
	unsigned char bitno;
#if BRATE > 1200
	unsigned char	dly;
#else
	unsigned int	dly;
#endif
	//if (!RxData)
	//{
	for(;;) {
		while(RxData)
			continue;	/* wait for start bit */
		dly = DELAY(3)/2;
		do
			/* waiting in delay loop */ ;
		while(--dly);
		if(RxData)
			continue;	/* twas just noise */
		bitno = 8;
		ca = 0;
		do {
			dly = DELAY(RX_OHEAD);
			do
			/* waiting in delay loop */ ;
			while(--dly);
			ca = (ca >> 1) | (RxData << 7);
		} while(--bitno);
		
		break;
	}
	//}	

	return ca;
}

char
getche(void)
{
	char c;

	putch(c = getch());
	return c;
}

