package TrabalhoModel;
import java.time.LocalDate;
import java.util.Calendar;
public class Emprestimo {

	

	private LocalDate data;
	private String prazo;
	private String date;
	private Livro livro;
	private Usuario usuario;
	private String data_entrega;
	private String situacao;
	private int id_emprestimo;
	
public int getId_emprestimo() {
		return id_emprestimo;
	}



	public void setId_emprestimo(int id_emprestimo) {
		this.id_emprestimo = id_emprestimo;
	}



public String getData_entrega() {
		return data_entrega;
	}



	public void setData_entrega(String data_entrega) {
		this.data_entrega = data_entrega;
	}



	public String getSituacao() {
		return situacao;
	}



	public void setSituacao(String situacao) {
		this.situacao = situacao;
	}



public Emprestimo(Livro livro, Usuario usuario) {
	setLivro(livro);
	setUsuario(usuario);
	
}



public Livro getLivro() {
	return livro;
}






public void setLivro(Livro livro) {
	this.livro = livro;
}


public Usuario getUsuario() {
	return usuario;
}









public void setUsuario(Usuario usuario) {
	this.usuario = usuario;
}









public String getPrazo() {
	return prazo;
}




public void setPrazo(String prazo) {
	this.prazo = prazo;
}




public String getDate() {
	return date;
}




public void setDate(String date) {
	this.date = date;
}









public String retorna_dados() {
	
	
	return "\nCpf do Usuário: "+usuario.getCpf()+
			"\nNome do usuário: "+usuario.getNome()+
			"\nCódigo ISBN do livro: "+livro.getIsbn()+
			"\nTítulo do Livro: "+livro.getTitulo()+
			"\nData do empréstimo: "+ this.date+
			"\nData para entrega: "+this.prazo+
			"\nSituação: "+this.situacao;
		
	
	
}


	
}
