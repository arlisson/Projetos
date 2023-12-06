package builder;

public class Principal {

	public static void main(String[] args) {


		Pessoa p = new PessoaBuilder()
				.nome("João")
				.cpf("000000000")
				.endereco(new EnderecoBuilder()
						.rua("Rua dos bobos")
						.numero(0)
						.complemento("Não tem ninguém")
						.builder())
				.rg("00000000000")
				.estadoCivil("Casado").builder();
		
		System.out.println(p);
	}

}
