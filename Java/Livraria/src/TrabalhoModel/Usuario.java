package TrabalhoModel;

public class Usuario {
	
	private String nome;
	private String cpf;
	private String endereco;
	private static int qtd;
	
	
	public Usuario (String nome, String cpf, String endereco ){
		
		this.nome = nome.toUpperCase();
		this.endereco = endereco.toUpperCase();	
		this.cpf = cpf.replace(".","").replace("-","").replace(" ","");
		
				
	}

	public int get_qtd() {
		return qtd;
	}
	
	
	public String getNome() {
		return this.nome;
	}

	

	public String getCpf() {
		return cpf.replace(".","").replace("-","").replace(" ","");
	}

	

	public String getEndereco() {
		return endereco;
	}

	public String get_dados() {		
		return "\nNome: "+this.nome +
				"\nCPF: " +this.cpf+
				"\nEndereço: "+this.endereco;
				
	
	}
	



	
}
