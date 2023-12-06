package decorator;

public class Leite extends Condimento{
	public Leite(Bebida bebida)
	{
		setBebida(bebida);
	}
	
	public String getDescricao()
	{
		return getBebida().getDescricao() + " + Leite";
	}
	
	public double valor()
	{
		return getBebida().valor() + 0.78;
	}
}
