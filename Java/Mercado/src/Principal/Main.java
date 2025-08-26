package Principal;

import DAO.ProdutoDAO;
import java.util.Scanner;

import Controller.*;

public class Main {
    public static void main(String[] args) {
       
    
    	Scanner scanner = new Scanner(System.in);

        String[] opcoes = {
            "1 - Gestão",
            "2 - Comprar",
            "3 - Sair"
        };

        int opcao;

        do {
        	Funcoes.MenuOpcoes(opcoes, "Principal");
           
            opcao = scanner.nextInt();
            scanner.nextLine(); // consumir \n

            switch (opcao) {
                case 1:
	                Funcoes.MenuGestao(scanner);
		            break;
		        
                case 2:
                	Funcoes.simularCompra(scanner);
                	break;

                default:                	
                    System.out.println("Opção inválida!");
            }

        } while (opcao != 3);

        scanner.close();   
    }    
          
    
   
}
