package strategy;

public class CalculadoraIPVA {
	IPVAStrategy strategy;
	
	public CalculadoraIPVA(IPVAStrategy strategy) {
		this.setStrategy(strategy);
	}
	
	public void setStrategy(IPVAStrategy strategy) {
		this.strategy = strategy;
	}
	
	public double calcular(Veiculo veiculo) {
		return strategy.calcular(veiculo);
	}

}
