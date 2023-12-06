:DECLARACOES

numero: INT
fatorial: INT

:ALGORITMO

LER numero

ATRIBUIR numero A fatorial

SE numero = 0 ENTAO
	INICIO 
		ATRIBUIR 1 A fatorial
	FIM
	
ENQUANTO numero > 1
	INICIO 
		ATRIBUIR fatorial * (numero -1 ) A fatorial
		ATRIBUIR numero -1 A numero
	FIM

IMPRIMIR fatorial