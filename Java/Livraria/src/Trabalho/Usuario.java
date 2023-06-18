package Trabalho;

public class Usuario {
	
	private String nome;
	private String cpf;
	private String endereco;
	private static int qtd;
	
	
	public Usuario (String nome, String cpf, String endereco ){
		
		this.nome = nome;
		this.endereco = endereco;	
		this.cpf = cpf.replace(".","").replace("-","").replace(" ","");
		valida_cpf(cpf);
		qtd++;
		
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
		return "Nome: "+this.nome +
				"\nCPF: " +this.cpf+
				"\nEndereço: "+this.endereco;
				
	
	}
	

static Boolean valida_cpf(String cpf) {
	
	cpf = cpf.replace(".","").replace("-","").replace(" ","");
		
	
	if(cpf.length()!=11) {		
		return false;
	}
	
	
	int aux =0;	
	for (int i = 0; i<9; i++) {		
		aux += Character.getNumericValue(cpf.charAt(i)) * (10-i);
		
	}
	
	int r = aux%11;
	if( r <2) {
		if(Character.getNumericValue(cpf.charAt(9))!=0) {
			return false;
		}
		
	}else if ((11 - r) != Character.getNumericValue(cpf.replace(".","").replace("-","").charAt(9))) {
		return false;
		
	}
	r =0;
	aux = 0;
	for (int i = 0; i<10; i++) {		
		aux += Character.getNumericValue(cpf.charAt(i)) * (11-i);
		
	}
	
	r = aux%11;
	if( r <2) {
		if(Character.getNumericValue(cpf.charAt(10))!=0) {
			return false;
		}
		
	}else if ((11 - r) != Character.getNumericValue(cpf.replace(".","").replace("-","").charAt(10))) {
		return false;
		
	}
	
	
	
	return true;
		
	}

	
}
