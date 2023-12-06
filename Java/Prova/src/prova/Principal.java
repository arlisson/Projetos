package prova;

import java.time.LocalDateTime;
import java.util.Scanner;
import java.util.ArrayList;

public class Principal {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		Scanner sc = new Scanner(System.in);
		
		ArrayList<Ticket> tickets = new ArrayList<Ticket>();
		LogManager log = LogManager.getInstance();
		
		int escolha = 0, codigo_ticket=1, parcelas;
		String cpf,numero_cartao;
		Double valor = 15.0, valor_pago;
		boolean encontrado = false;
		while(escolha != 4) {
			System.out.println("\nO que deseja fazer?\n1 - Estacionar\n2 - Deixar estacionamento\n3 - Ver tickets em aberto\n4 - Sair");
			escolha = sc.nextInt();
			
			switch(escolha) {
			
			case 1:
			
				tickets.add(new Ticket(codigo_ticket, LocalDateTime.now()));
				
				System.out.println("\nEstacionado, Código do Ticket: "+codigo_ticket);
				
				codigo_ticket++;			
			break;
			
			case 2:
				
				System.out.println("\nInforme o código do ticket: ");
				escolha = sc.nextInt();
				
				for(Ticket t: tickets) {
					if(t.getCodigo()==escolha && t.isRetirado()==false) {		
						encontrado = true;				
						System.out.println("\nDeseja inserir o CPF na Nota Fiscal?\n1 - Sim\n2 - Não");
						escolha=sc.nextInt();
						
						switch(escolha) {
						case 1:
							
							System.out.println("\nDigite o CPF: ");
							cpf = sc.next();
							log.setCpf(cpf);
							System.out.println("\nQual a forma de Pagamento?\n1 - Débito\n2 - Crédito\n3 - Dinheiro");
							escolha = sc.nextInt();
							switch(escolha) {
							
							case 1:
								System.out.println("\nInforme o número do cartão: ");
								numero_cartao = sc.next();
								Debito debito = new Debito(numero_cartao);
								log.setPagamento(debito);
								t.setData_f(LocalDateTime.now());
								log.setTicket(t);
								System.out.println(log.toString());
								log.NotaFiscal();
								t.setRetirado(true);
								System.out.println("Retirada de carro concluída com sucesso!");
							break;
							
							case 2:
								System.out.println("\nInforme o número do cartão: ");
								numero_cartao = sc.next();
								System.out.println("\nInforme a quantidade de parcelas");
								parcelas = sc.nextInt();
								Credito credito = new Credito(numero_cartao,parcelas);
								log.setPagamento(credito);
								t.setData_f(LocalDateTime.now());
								log.setTicket(t);
								System.out.println(log.toString());
								log.NotaFiscal();
								System.out.println("Retirada de carro concluída com sucesso!");
								t.setRetirado(true);
							break;
							
							case 3:
								System.out.println("\nInforme o valor pago: ");
								valor_pago = sc.nextDouble();
								if(valor_pago<15) {
									System.out.println("Valor pago invalido!");
								}else if(valor_pago>valor) {
									Dinheiro dinheiro = new Dinheiro(valor_pago,(valor_pago-valor));
									log.setPagamento(dinheiro);
									t.setData_f(LocalDateTime.now());
									log.setTicket(t);
									System.out.println(log.toString());
									log.NotaFiscal();
									System.out.println("Retirada de carro concluída com sucesso!");
									t.setRetirado(true);
								}else {
									Dinheiro dinheiro = new Dinheiro(valor_pago,0.0);
									log.setPagamento(dinheiro);
									t.setData_f(LocalDateTime.now());
									log.setTicket(t);
									System.out.println(log.toString());
									log.NotaFiscal();
									System.out.println("Retirada de carro concluída com sucesso!");
									t.setRetirado(true);
								}
								
								break;
								
							}
							
							
						break;
						
						case 2:
							
							System.out.println("\nQual a forma de Pagamento?\n1 - Débito\n2 - Crédito\n3 - Dinheiro");
							escolha = sc.nextInt();
							switch(escolha) {
							
							case 1:
								System.out.println("\nInforme o número do cartão: ");
								numero_cartao = sc.next();
								Debito debito = new Debito(numero_cartao);
								log.setPagamento(debito);
								t.setData_f(LocalDateTime.now());
								log.setTicket(t);
								System.out.println(log.toString());
								log.NotaFiscal();
								System.out.println("Retirada de carro concluída com sucesso!");
								t.setRetirado(true);
							
							break;
							
							case 2:
								System.out.println("\nInforme o número do cartão: ");
								numero_cartao = sc.next();
								System.out.println("\nInforme a quantidade de parcelas");
								parcelas = sc.nextInt();
								Credito credito = new Credito(numero_cartao,parcelas);
								log.setPagamento(credito);
								t.setData_f(LocalDateTime.now());
								log.setTicket(t);
								System.out.println(log.toString());
								log.NotaFiscal();
								System.out.println("Retirada de carro concluída com sucesso!");
								t.setRetirado(true);
							break;
							
							case 3:
								System.out.println("\nInforme o valor pago: ");
								valor_pago = sc.nextDouble();
								if(valor_pago<15) {
									System.out.println("Valor pago invalido!");
								}else if(valor_pago>valor) {
									Dinheiro dinheiro = new Dinheiro(valor_pago,(valor_pago-valor));
									log.setPagamento(dinheiro);
									t.setData_f(LocalDateTime.now());
									log.setTicket(t);
									System.out.println(log.toString());
									log.NotaFiscal();
									System.out.println("Retirada de carro concluída com sucesso!");
									t.setRetirado(true);
								}else {
									Dinheiro dinheiro = new Dinheiro(valor_pago,0.0);
									log.setPagamento(dinheiro);
									t.setData_f(LocalDateTime.now());
									log.setTicket(t);
									System.out.println(log.toString());
									log.NotaFiscal();
									System.out.println("Retirada de carro concluída com sucesso!");
									t.setRetirado(true);
								}
								
								break;
								
							}
							
							
						break;
						}					
						
					}
							
				}
				if(encontrado==false) {
					System.out.println("\nTicket não encontrado!");
					break;
				}		
				
				
			break;
			
			case 3:
				if(tickets.size()==0) {
					System.out.println("Nenhum ticket registrado!");
				}else {
					for(Ticket t : tickets) {
						if(t.isRetirado()) {
							System.out.println("\nID: "+t.getCodigo()+"\nData e hora de entrada: "+ t.getData_i()+"\nSituaçao: Retirado");
						}else {
							System.out.println("\nID: "+t.getCodigo()+"\nData e hora de entrada: "+ t.getData_i()+"\nSituaçao: Em aberto");
						}
						
					}
				}
				
			
			}
			
			
			
			
		}

	}

}
