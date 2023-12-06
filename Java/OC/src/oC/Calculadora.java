package oC;

public class Calculadora {
	private Operacao operacao;
	
	public Calculadora(Operacao operacao) {
		this.operacao = operacao;
	}
	
	
	public double calcular(double a, double b) {
		return operacao.Calcular(a, b);
	}
}
