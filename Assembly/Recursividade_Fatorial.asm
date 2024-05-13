.data
n: .asciz "\n"
.text
.global main

main:
	li a0 4
	jal ra fatorial
	
	li a7 1	
	ecall 
	
	li a7 93
	ecall

fatorial:
	addi sp sp -8 # Decrementa o ponteiro de pilha para salvarespaco para ra e a0
	sw ra 4(sp) # Salva o conteudo do registrador ra na p i l h a
	sw a0 0(sp) # Salva o conteudo do registrador a0 na p i l h a
	
	li a1 1
	beq a0 a1 base_case
	li a1 0 
	beq a0 a1 base_case
	
	
	
	addi a0 a0 -1
	jal ra fatorial #chamada recursiva
	lw a1 0(sp) #Recuperar o Vaor Original de n
	mul a0 a0 a1 #n * fatorial(n-1)
	
	
	
	
	
	lw ra 4(sp) #Recuperar o Vaor Original de ra
	addi sp sp 8
	ret
	
base_case:
	li a0 1 # O f a t o r i a l de 1 ou 0 e 1
	lw ra 4 (sp) # Restaurar o v a lo r o r i g i n a l de ra
	addi sp sp 8 # Restaurar o ponteiro da p i l h a
	ret # Retornar ao endereco salvo em ra
	
	
	
	
