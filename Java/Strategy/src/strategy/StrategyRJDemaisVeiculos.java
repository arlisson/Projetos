package strategy;
public class StrategyRJDemaisVeiculos extends RJStrategy {
	
	public double calcularIPVA(Veiculo veiculo) {
		return veiculo.getValor() * 0.04;
	}

}
