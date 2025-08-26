package Controller;
import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Scanner;

import DAO.ProdutoDAO;
import Model.Carrinho;
import Model.Produto;
public class Funcoes {
	
	public static void InserirProduto(String nome, double preco) {
		ProdutoDAO.inserirProduto(nome, preco);
		
	}
	
	public static void ListarTodos (){
		 List<Produto> produtos = ProdutoDAO.listarProdutos();
         System.out.println("\n--- Lista de Produtos ---");
         for (Produto p : produtos) {
             System.out.println(p);
         }
		 
	}
	
	public static void MenuOpcoes (String[] opcoes, String menu){
		System.out.println("\n=== Menu "+menu+" ===");
		for (String opcao : opcoes) {
	        System.out.println(opcao);
	    }
        
        System.out.print("Escolha uma opção: ");
	}
	
	public static void MenuGestao(Scanner scanner) {
        int opcao;
       
        
        do {
        	MenuOpcoes(new String[] {"1 - Cadastrar Produto","2 - Listar Produtos","3 - Voltar"}, "Gestão");      
            
            opcao = scanner.nextInt();
            scanner.nextLine();

            switch (opcao) {
                case 1:
                    System.out.print("Nome do produto: ");
                    String nome = scanner.nextLine();

                    System.out.print("Preço do produto: ");
                    String precoStr = scanner.nextLine().replace(",", ".");
                    double preco;

                    try {
                        preco = Double.parseDouble(precoStr);
                        ProdutoDAO.inserirProduto(nome, preco);
                    } catch (NumberFormatException e) {
                        System.out.println("Preço inválido. Use ponto ou vírgula corretamente.");
                    }
                    break;


                case 2:
                	ListarTodos();
                    break;

                case 3:
                    System.out.println("Voltando ao menu principal...");
                    break;

                default:
                    System.out.println("Opção inválida!");
                    break;
            }

        } while (opcao != 3);
    }
	
	public static void simularCompra(Scanner scanner) {
	    Carrinho carrinho = new Carrinho();

	    while (true) {
	    	MenuOpcoes(new String[] {"1 - Adicionar produto ao carrinho","2 - Ver carrinho","3 - Cancelar compra","4 - Finalizar compra"},"de Compras");

	        
	       
	        int opcao = scanner.nextInt();
	        scanner.nextLine();

	        switch (opcao) {
	            case 1:
	                System.out.print("Digite o ID do produto: ");
	                int id = scanner.nextInt();
	                scanner.nextLine();

	                Produto escolhido = ProdutoDAO.buscarProdutoId(id);
	                if (escolhido != null) {
	                    carrinho.adicionar(escolhido);
	                    System.out.println("Produto adicionado ao carrinho: " + escolhido.getNome());
	                } else {
	                    System.out.println("Produto não encontrado.");
	                }
	                break;

	            case 2:
	                carrinho.exibirResumo();
	                break;

	            case 3:
	                System.out.println("Compra cancelada. Carrinho esvaziado.");
	                carrinho.limpar();
	                return;

	            case 4:
	                carrinho.exibirResumo();
	                System.out.println("Compra finalizada!");
	                gerarNota(carrinho);
	                return;

	            default:
	                System.out.println("Opção inválida.");
	        }
	    }
	}
	
	public static void gerarNota(Carrinho carrinho) {
        String nomeArquivo = "nota_fiscal_" + LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss")) + ".txt";

        try (FileWriter writer = new FileWriter(nomeArquivo)) {
            writer.write("===== NOTA FISCAL =====\n");
            writer.write("Data: " + LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss")) + "\n\n");

            for (Produto p : carrinho.getItens()) {
                writer.write(String.format("%-20s R$ %.2f\n", p.getNome(), p.getPreco()));
            }

            writer.write("\n------------------------\n");
            writer.write(String.format("Quantidade: %d\n", carrinho.getQuantidade()));
            writer.write(String.format("Total:      R$ %.2f\n", carrinho.getTotal()));
            writer.write("========================\n");

            System.out.println("Nota fiscal salva em: " + nomeArquivo);

        } catch (IOException e) {
            System.out.println("Erro ao gerar nota fiscal: " + e.getMessage());
        }
    }
}

	

