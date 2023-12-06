package prova;

public class Debito implements Pagamento{
	
	private String num_cartao;
	
	@Override
	public String Pagar() {
		// TODO Auto-generated method stub
		return "Débito";
	}
	
	public Debito(String num_cartao) {
		this.num_cartao = num_cartao;
	}

	@Override
	public String toString() {
		return "\nNúmero do Cartão:" + num_cartao + "\nForma de Pagamento: " + Pagar();
	}

	
	
}
