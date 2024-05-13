.data
	origem: .asciz " A "
	auxiliar: .asciz " B "
	destino: .asciz " C "
	mova: .asciz "Mova o disco "
	para: .asciz " para "
	de: .asciz " de "
	n: .asciz "\n"
	hanoi: .asciz " torre_hanoi "
	hanoi2: .asciz " torre_hanoi2 "
	base: .asciz " base "
	case: .asciz " max_case "	
.text
.global main

main:	
	li a0 3
	li a4 3
	
	la a1 origem
	la a2 auxiliar
	la a3 destino
	jal ra torre_hanoi	
	
	li a7 93
	ecall
	
torre_hanoi:
	
	addi sp sp -8 # Decrementa o ponteiro de pilha para salvarespaco para ra e a0
	sw ra 4(sp) # Salva o conteudo do registrador ra na p i l h a
	sw a0 0(sp) # Salva o conteudo do registrador a0 na p i l h a	
	
	
	
	li t1 1
	beq a0 t1 base_case #Caso base		
	
		
	addi a0 a0 -1		
	
	
	jal ra torre_hanoi #Chamada Recursiva		
	lw a0 0(sp)
	beq a0 a4 max_case #Caso base	
	
					
	li a7 4
	la a0 mova
	ecall
	
	li a7 1
	lw a0 0(sp) #Recuperar o Vaor Original de a0, no caso, o valor que foi salvo em 0(sp)
	ecall
	
	li a7 4
	la a0 de
	ecall
	
	li a7 4
	mv a0 a1
	ecall	
	
	li a7 4
	la a0 para
	ecall	
	
	li a7 4
	mv a0 a3
	ecall
	
	li a7 4
	la a0 hanoi
	ecall	
	
	li a7 4
	la a0 n
	ecall
	
	mv t0 a2
	mv a2 a1
	mv a1 t0
				
	lw a0 0(sp)
	addi a0 a0 -1	
	jal ra torre_hanoi	
	
	lw a0 0(sp)		
	lw ra 4 (sp) # Restaurar o valor original de ra
	addi sp sp 8 # Restaurar o ponteiro da p i l h a	
				
	ret # Retornar ao endereco salvo em ra
	
	

base_case:	
	li a7 4
	la a0 mova
	ecall
	
	li a7 1
	li a0 1
	ecall
	
	li a7 4
	la a0 de
	ecall
	
	li a7 4
	mv a0 a1
	ecall	
	
	li a7 4
	la a0 para
	ecall	
	
	li a7 4
	mv a0 a3
	ecall	
	
	li a7 4
	la a0 base
	ecall	
	
	li a7 4
	la a0 n
	ecall	
	
	mv t0 a3
	mv a3 a2
	mv a2 t0	
		
	lw a0 0(sp)	
	lw ra 4 (sp) # Restaurar o valor original de ra	
	addi sp sp 8 # Restaurar o ponteiro da p i l h a
	ret # Retornar ao endereco salvo em ra
		
max_case:
	li a7 4
	la a0 mova
	ecall
	
	li a7 1
	mv a0 a4
	ecall
	
	li a7 4
	la a0 de
	ecall
	
	li a7 4
	la a0 origem
	ecall	
	
	li a7 4
	la a0 para
	ecall	
	
	li a7 4
	la a0 destino
	ecall	
	
	li a7 4
	la a0 case
	ecall	
	
	
	li a7 4
	la a0 n
	ecall	
	
	
	mv t0 a2
	mv a2 a1
	mv a1 t0
	
	lw a0 0(sp)
	addi a0 a0 -1	
	jal ra torre_hanoi			
							
	lw a0 0(sp)	
	lw ra 4 (sp) # Restaurar o valor original de ra
	addi sp sp 8 # Restaurar o ponteiro da p i l h a
	ret # Retornar ao endereco salvo em ra