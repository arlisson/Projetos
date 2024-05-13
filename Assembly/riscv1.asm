.data
	msg_1: .asciz "Informe o primeiro numero: "
	msg_2: .asciz "Informe o segundo numero: "
	resultado: .asciz "Resultado: "
  
.text 
.global main
main:
	li a7 4		 
	la a0 msg_1
	ecall #imprime a mensagem do primeiro número
		 
	li a7 5 
	ecall
	mv t0 a0 #move o valor de a0 para t0
	 
	li a7 4
	la a0 msg_2
	ecall
	 
	li a7 5 
	ecall
	mv t1 a0
	 
	add t2 t0 t1 
	 
	li a7 4
	la a0 resultado
	ecall
	 
	li a7 1
	mv a0 t2 #move o valor de t2 para a0
	ecall
	
