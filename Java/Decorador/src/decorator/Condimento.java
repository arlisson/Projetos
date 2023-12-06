package decorator;

public abstract class Condimento extends Bebida{
	
	private Bebida bebida;

	public void setBebida(Bebida bebida) {
		this.bebida = bebida;
	}

	public Bebida getBebida() {
		return bebida;
	}
	
}
