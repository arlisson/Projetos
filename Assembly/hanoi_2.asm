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
	li a0 4
	li a4 4
	
	la a1 origem
	la a2 auxiliar
	la a3 destino
	jal ra torre_hanoi	
	
	li a7 93
	ecall
	
torre_hanoi:
	
	addi sp sp -20 # Decrementa o ponteiro de pilha para salvarespaco para ra e a0
	sw ra 16(sp) # Salva o conteudo do registrador ra na p i l h a
	sw a3 12(sp)
	sw a2 8(sp)
	sw a1 4(sp)
	sw a0 0(sp) # Salva o conteudo do registrador a0 na p i l h a		
	
	
							
	li t1 1
	beq a0 t1 base_case #Caso base	
					
	addi a0 a0 -1	
	
	#################################
	# Recuperando os valores	#
	# passados como parâmetro	#
	# e alternando os valores	#
	# 				#	
 	#################################
	lw a1 4(sp)
	lw a3 8(sp)
	lw a2 12(sp)	
	
	jal ra torre_hanoi #Chamada Recursiva		
	
	#################################
	# Recuperando os valores	#
	# passados como parâmetro	#
	# e alternando os valores	#
	# 				#	
 	#################################	
				
	lw a0 0(sp)
	lw a1 4(sp)
	lw a2 8(sp)
	lw a3 12(sp)	
					
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
	#################################
	#				#
	# Recuperando os valores	#
	# passados como parâmetro	#
	# 				#	
 	#################################
	lw a0 0(sp)  
	lw a2 4(sp)
	lw a1 8(sp)
	lw a3 12(sp)			
													
	
	addi a0 a0 -1	
	jal ra torre_hanoi	
	
	
	lw ra 16 (sp) # Restaurar o valor original de ra	
	addi sp sp 20 # Restaurar o ponteiro da p i l h a
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
	
		
	lw a0 0(sp) 	#################################
	lw a1 4(sp)	#				#
	lw a2 8(sp)	# Recuperando os valores	#
	lw a3 12(sp)	# passados como parâmetro	#
	lw ra 16 (sp)	# 				#	
	addi sp sp 20 	#################################
	ret # Retornar ao endereco salvo em ra