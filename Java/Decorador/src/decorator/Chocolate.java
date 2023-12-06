package decorator;

public class Chocolate extends Condimento{

	public Chocolate(Bebida bebida) {
		setBebida(bebida);
	}
	
	public String getDescricao()
	{
		return getBebida().getDescricao() + " + Chocolate";
	}
	
	public double valor()
	{
		return getBebida().valor() + 0.5;
	}
}