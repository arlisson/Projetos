package data;

import java.util.Scanner;
import java.time.LocalDate;
public class Principal {

	public static void main(String[] args) {
		
		int dia, mes, ano;
		LocalDate data = LocalDate.now();
		Scanner sc = new Scanner(System.in);					
		
		System.out.println("Digite o dia: ");		
		dia = sc.nextInt();
		System.out.println("Digite o mes: ");
		mes = sc.nextInt();
		System.out.println("Digite o ano: ");
		ano = sc.nextInt();
		if(Data.verifica_ano(ano)) {
			if(Data.verifica_mes(mes)) {
				if(Data.verifica_dia(dia, mes, ano)) {
					System.out.println("Data aceita");
				}else {
					System.out.println("Dia inválido!");
				}
			}else {
				System.out.println("Mes inválido!");
			}
		}else {
			System.out.println("Ano inválido!");
		}
			
	
		
		
	}

}
