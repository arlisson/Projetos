package builder;

public class PessoaBuilder {
	private Pessoa pessoa;
	
	public PessoaBuilder() {
		this.pessoa = new Pessoa();
	}
	
	public Pessoa builder() {
		return pessoa;
	}
	
	public PessoaBuilder nome(String nome) {
		this.pessoa.setNome(nome);
		return this;
	}
	
	public PessoaBuilder cpf(String cpf) {
		this.pessoa.setCpf(cpf);
		return this;
	}
	
	public PessoaBuilder rg(String rg) {
		this.pessoa.setRg(rg);
		return this;
	}
	
	public PessoaBuilder endereco(Endereco endereco) {
		this.pessoa.setEndereco(endereco);
		return this;
	}
	public PessoaBuilder estadoCivil(String estado) {
		this.pessoa.setEstado_civil(estado);
		return this;
	}
	
}
