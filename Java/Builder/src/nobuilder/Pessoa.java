package nobuilder;

public class Pessoa {
	private String nome;
	private String cpf;
	private String rg;
	private Endereco endereco;
	private String estado_civil;
	
	
	public Pessoa(String nome, String cpf, String rg, Endereco endereco, String estado_civil) {		
		this.nome = nome;
		this.cpf = cpf;
		this.rg = rg;
		this.endereco = endereco;
		this.estado_civil = estado_civil;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public String getCpf() {
		return cpf;
	}

	public void setCpf(String cpf) {
		this.cpf = cpf;
	}

	public String getRg() {
		return rg;
	}

	public void setRg(String rg) {
		this.rg = rg;
	}

	public Endereco getEndereco() {
		return endereco;
	}

	public void setEndereco(Endereco endereco) {
		this.endereco = endereco;
	}

	public String getEstado_civil() {
		return estado_civil;
	}

	public void setEstado_civil(String estado_civil) {
		this.estado_civil = estado_civil;
	}
	
	@Override
	public String toString() {
		// TODO Auto-generated method stub
		return "\nNome: "+getNome() +"\nCPF: "+getCpf()+"\nRG: "+getRg()+"\nEstaod Civil: "+getEstado_civil()+"\n----Endereco----\n"+getEndereco();
	}

}
