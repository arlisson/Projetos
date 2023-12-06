package decorator;

public class Principal {
	public static void main(String[] args){
		Bebida b = new Cafe();
		
		System.out.println(b.getDescricao() + " " + b.valor());
		
		b = new Chocolate(b);
		
		System.out.println(b.getDescricao() + " " + b.valor());
		
		b = new Leite(b);
		
		System.out.println(b.getDescricao() + " " + b.valor());
		
	}
	
}
