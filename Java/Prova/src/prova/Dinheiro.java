package prova;

public class Dinheiro implements Pagamento{
	
	private Double valor;
	private Double troco;
	@Override
	public String Pagar() {
		// TODO Auto-generated method stub
		return "Dinheiro";
	}
	
	public Dinheiro(Double valor, Double troco) {
		this.valor = valor;
		this.troco = troco;
	}

	@Override
	public String toString() {
		return "\nValor Pago: R$" + valor + "\nValor do Troco: R$" + troco + "\nMétodo de pagamento: " + Pagar();
	}
	
	

}
