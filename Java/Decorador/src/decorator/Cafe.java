package decorator;

public class Cafe extends Bebida{

	public Cafe() {

		setDescricao("Café");
	}
			
	@Override
	public double valor() {
		// TODO Auto-generated method stub
		return 1.5;
	}
	
}
