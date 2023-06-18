package Trabalho;
import java.time.LocalDate;
import java.util.Calendar;
public class Emprestimo {

	private String nome_usuario;
	private String titulo_livro;
	private String cpf_usuario;
	private String ibn_livro;
	private LocalDate data;
	private int qtd=0;
	private int prazo;

	
public Emprestimo(String nome_usuario, String titulo_livro, String cpf_usuario, String isbn_livro, LocalDate data, int prazo) {
	
	this.cpf_usuario = cpf_usuario;
	this.nome_usuario = nome_usuario;
	this.titulo_livro = titulo_livro;
	this.ibn_livro = isbn_livro;
	this.data = data;
	this.prazo = prazo;
	qtd++;
}
	

public String getNome_usuario() {
	return nome_usuario;
}


public String getTitulo_livro() {
	return titulo_livro;
}


public String getCpf_usuario() {
	return cpf_usuario;
}


public String getIbn_livro() {
	return ibn_livro.replace(" ", "").replace("-", "");
}

public int getQtd(){
	return qtd;
}



public String retorna_dados() {
	
	
	return "Nome do Usuário: "+this.nome_usuario+
			"\nTítulo do Livro: "+this.titulo_livro+
			"\nCpf do Usuário: "+this.cpf_usuario+
			"\nCódigo ISBN do livro: "+this.ibn_livro+
			"\nData do empréstimo: "+ this.data+
			"\nData de entrega: "+this.data.plusDays(prazo);
	
	
}

public boolean verifica_atraso() {
	
	if(data.now().isAfter(this.data.plusDays(prazo))) {
		return true;
	}
	return false;
	
}
	
}
