package prova;

public class Credito implements Pagamento{
	
	private String num_cartao;
	private int parcelas;
	
	@Override
	public String Pagar() {
		// TODO Auto-generated method stub
		return "Crédito";
		
	}

	public Credito(String num_cartao, int parcelas) {
		
		this.num_cartao = num_cartao;
		this.parcelas = parcelas;
	}

	@Override
	public String toString() {
		return "\nNúmero do Cartão: " + num_cartao + "\nParcelas: " + parcelas + "\nMétodo de pagamento: " + Pagar();
	}
	
	
	

}
