package strategy;

public abstract class RJStrategy implements IPVAStrategy {
	
	public final double calcular (Veiculo veiculo) {
		if (veiculo.getAno() - 2023 <= 15) {
			return calcularIPVA(veiculo);
		}
		return 0;
	}
	
	public abstract double calcularIPVA(Veiculo veiculo);

}
