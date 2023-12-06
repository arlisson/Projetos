package oC;

public class Principal {

	public static void main(String[] args) {
		
		System.out.println(new Calculadora(new Soma()).calcular(2, 2));
		System.out.println(new Calculadora(new Subtrair()).calcular(2, 2));
	}

}
