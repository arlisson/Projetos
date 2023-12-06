package strategy;

public class Principal {
	public static void main(String[] args) {
		Veiculo veiculo = new Veiculo();
		veiculo.setAno(2020);
		veiculo.setValor(100000);
		veiculo.setEstado("RJ");
		veiculo.setCombustivel("Gasolina");
		
		CalculadoraIPVA calculadora;
		
		if (veiculo.getEstado().equals("RJ")) {
			if (veiculo.getCombustivel().equals("Gasolina")) {
				calculadora = new CalculadoraIPVA(new StrategyRJDemaisVeiculos());
				System.out.println(calculadora.calcular(veiculo));
			}
		}
		
		
		
	}
}
