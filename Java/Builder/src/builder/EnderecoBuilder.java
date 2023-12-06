package builder;

public class EnderecoBuilder {
	
	private Endereco endereco;
	
	public EnderecoBuilder() {
		this.endereco = new Endereco();
	}
	
	public Endereco builder() {
		return endereco;
	}

	public EnderecoBuilder rua(String rua) {
		this.endereco.setRua(rua);
		return this;
	}
	public EnderecoBuilder numero(int numero) {
		this.endereco.setNumero(numero);
		return this;
	}
	
	public EnderecoBuilder complemento(String complemento) {
		this.endereco.setComplemento(complemento);
		return this;
	}
}
