package Trabalho;

import java.util.ArrayList;
import java.util.Scanner;
import java.time.LocalDate;
import java.util.Calendar;
public class Principal {	

	public static void main(String[] args) {		
		
		Scanner sc = new Scanner(System.in);
		ArrayList<Usuario> usuarios = new ArrayList<Usuario>(); 
		ArrayList<Livro> livros = new ArrayList<Livro>(); 
		ArrayList<Emprestimo> emprestimos = new ArrayList<Emprestimo>();		
		
		usuarios.add(new Usuario("Árlisson","111.111.111","GROSSO"));		
		usuarios.add(new Usuario("Maria", "222.222.222-22", "Av. B, 456"));
        usuarios.add(new Usuario("Pedro", "333.333.333-33", "Travessa C, 789"));
        usuarios.add(new Usuario("Ana", "444.444.444-44", "Alameda D, 101"));
        usuarios.add(new Usuario("Lucas", "555.555.555-55", "Praça E, 234"));
        usuarios.add(new Usuario("Julia", "666.666.666-66", "Rodovia F, 567"));
        usuarios.add(new Usuario("Fernanda", "777.777.777-77", "Avenida G, 890"));
        usuarios.add(new Usuario("Rafael", "888.888.888-88", "Estrada H, 111"));
        usuarios.add(new Usuario("Mariana", "999.999.999-99", "Largo I, 222"));
        usuarios.add(new Usuario("Carlos", "000.000.000-00", "Viela J, 333"));
        
        livros.add(new Livro("Cem Anos de Solidão", "978-8501012074", "Editora Record", "Realismo Mágico"));
        livros.add(new Livro("Dom Casmurro", "978-6586490084", "Companhia das Letras", "Romance"));
        livros.add(new Livro("1984", "978-8535914849", "Companhia Editora Nacional", "Ficção Distópica"));
        livros.add(new Livro("A Revolução dos Bichos", "978-8535909555", "Companhia das Letras", "Fábula Política"));
        livros.add(new Livro("O Pequeno Príncipe", "978-8581303079", "Geração Editorial", "Infantojuvenil"));
        livros.add(new Livro("O Nome do Vento", "978-6555651850", "Arqueiro", "Fantasia"));
        livros.add(new Livro("A Menina que Roubava Livros", "978-8598078175", "Intrínseca", "Drama"));
        livros.add(new Livro("Orgulho e Preconceito", "978-8567097787", "Martin Claret", "Romance Clássico"));
        livros.add(new Livro("A Guerra dos Tronos", "978-8556510785", "LeYa", "Fantasia"));        
		livros.add(new Livro("As digitais dos deuses", "978-8501054715", "Record", "Ciência"));
		
		
		String nome = null, cpf, endereco, titulo = null, isbn, editora, categoria;
		int escolha = -1,prazo;
		LocalDate data = LocalDate.now();
		
		while(escolha != 0) {
			
			int aux = 0;
			System.out.println("--------------------O que deseja fazer?--------------------\n1-Cadastrar Usuário.\n2-Cadastrar Livro.\n3-Alugar Livro.\n4-Consultar Livro.\n5-Consultar Usuário.\n6-Exibir lista de empréstimos.\n0-Sair");
			escolha = sc.nextInt();
			switch(escolha) {
			case 1:	
				aux = 0;
				System.out.println("Digite o cpf: ");
				sc.nextLine();
				cpf = sc.nextLine();	
				for (Usuario usuario : usuarios) {
					 if(usuario.getCpf().equals(cpf.replace(".","").replace("-","").replace(" ",""))) {
						System.out.println("CPF já cadastrado!!");
						aux++;
					 }         
			       
				 }
				if(Usuario.valida_cpf(cpf) && aux ==0) {
						
						System.out.println("Digite o nome: ");						
						nome = sc.nextLine();						
						System.out.println("Digite o endereço: ");						
						endereco = sc.nextLine();						
						usuarios.add(new Usuario(nome,cpf,endereco));
						System.out.println("Usuário cadastrado com Suesso!");
					}else if(aux==0 && Usuario.valida_cpf(cpf)==false) {
						System.out.println("Cpf inválido!!");
						
					}
				break;
				
			
			case 2:
				aux =0;
				System.out.println("Digite o ISBN do livro: ");
				sc.nextLine();
				isbn = sc.nextLine();
				for (Livro livro : livros) {
					if(livro.getIsbn().equals(isbn.replace(" ", "").replace("-", ""))) {
						System.out.println("Livro já cadastrado!!");
						aux++;
					 }
			          
			     }
				if(Livro.verificaisbn(isbn.replace(" ", "").replace("-", "")) && aux==0) {
					System.out.println("Digite otítulo: ");
					titulo = sc.nextLine();
					System.out.println("Digite a editora: ");
					editora = sc.nextLine();
					System.out.println("Digite a categoria: ");
					categoria = sc.nextLine();
					System.out.println("Livro cadastrado com Suesso!");
					livros.add(new Livro(titulo,isbn,editora,categoria));
				}else if (Livro.verificaisbn(isbn.replace(" ", "").replace("-", ""))==false && aux==0) {
					System.out.println("ISBN inválido!!");
					
				}
				break;
				
			case 3:
			System.out.println("Digite o ISBN do livro: ");	
			String isbn1 = sc.next();
			if(livros.stream().anyMatch(livro -> livro.getIsbn().equals(isbn1.replace(" ", "").replace("-", "")))) {
				System.out.println("Digite o CPF do Usuário: ");
				String cpf1= sc.next();
				if(usuarios.stream().anyMatch(usuario -> usuario.getCpf().equals(cpf1.replace(".","").replace("-","").replace(" ","")))){
					for(Livro livro:livros) {
						if(livro.getIsbn().equals(isbn1.replace(" ", "").replace("-", ""))) {
							titulo = livro.getTitulo();
						}
					}
					for(Usuario usuario:usuarios) {
						if(usuario.getCpf().equals(cpf1.replace(".","").replace("-","").replace(" ",""))) {
							nome = usuario.getNome();
						}
					}				
					
					
				}else {
					System.out.println("CPF não encontrado!!");
					break;
				}
			System.out.println("Digite o prazo para entrega do Livro: ");
			prazo = sc.nextInt();
			emprestimos.add(new Emprestimo(nome,titulo,cpf1,isbn1, data, prazo));
			
			System.out.println("Emprestimo realizado com sucesso!\n------------------------------------\n");
			}else {
				System.out.println("ISBN não encontrado!!");
				break;
			}
			
				break;
			case 4:
				System.out.println("Digite o ISBN do Livro: ");
				String isbn2 = sc.next();
				if(livros.stream().anyMatch(livro -> livro.getIsbn().equals(isbn2.replace(" ", "").replace("-", "")))) {
					for (Livro livro : livros) {
						if(livro.getIsbn().equals(isbn2.replace(" ", "").replace("-", ""))) {
							System.out.println(livro.get_dados());
						}
					}
				if(emprestimos.stream().anyMatch(emprestimo -> emprestimo.getIbn_livro().equals(isbn2.replace(" ", "").replace("-", "")))) {
					System.out.println("Situação do Livro: Indisponível\n---------------------------------\n");
				}else {
					System.out.println("Situação do Livro: Disponível\n---------------------------------\n");
				}
				}else {
					System.out.println("Livro não encontrado!");
					break;
				}
				break;
			case 5:
				
				System.out.println("Digite o CPF do Usuário: ");
				String cpf2 = sc.next();
				if(usuarios.stream().anyMatch(usuario -> usuario.getCpf().equals(cpf2.replace(" ", "").replace("-", "").replace(".","")))) {
					for (Usuario usuario : usuarios) {
						if(usuario.getCpf().equals(cpf2.replace(" ", "").replace("-", "").replace(".",""))) {
							System.out.println(usuario.get_dados());
						}
					}
				if(emprestimos.stream().anyMatch(emprestimo -> emprestimo.getCpf_usuario().equals(cpf2.replace(" ", "").replace("-", "").replace(".","")))) {
					System.out.println("Situação do usuário: Possui livro emprestado\n---------------------------------\n");
				}else {
					System.out.println("Situação do usuário: Não possui livro emprestado\n---------------------------------\n");
				}
				}else {
					System.out.println("Usuário não encontrado!");
					break;
				}
				
				break;
				
				
			case 6:
				if(emprestimos.size() == 0) {
					System.out.println("Nenhum Empréstimo encontrado!");
				}else {
					for(Emprestimo emprestimo: emprestimos) {					
						System.out.println(emprestimo.retorna_dados());
						if(emprestimo.verifica_atraso()) {
							System.out.println("Situação do empréstimo: Atrasado");
							System.out.println("\n----------------------------------------\n");
						}else {
							System.out.println("Situação do empréstimo: Dentro do prazo");
							System.out.println("\n----------------------------------------\n");
						}
					}
				}
				
			}	
				
		
				
			}

		}
		
	}
