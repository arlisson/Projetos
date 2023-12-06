package nobuilder;

public class Principal {

	public static void main(String[] args) {


		Pessoa pessoa = new Pessoa("João","000000000","00000000000",new Endereco("Rua dos bobos",0, "Não tinha nada"),"Casado");
		
		System.out.println(pessoa);

	}

}
