package TrabalhoModel;

public class Livro {

	private String titulo;
	private String isbn;
	private String editora;
	private String categoria;
	private static int qtd;
	




public Livro (String titulo, String isbn, String editora, String categoria) {
	
	this.titulo = titulo.toUpperCase();
	this.editora = editora.toUpperCase();
	this.categoria = categoria.toUpperCase();		
	this.isbn = isbn.replace(" ", "").replace("-", "");
	
}



public String getTitulo() {
	return titulo;
}

public String getIsbn() {
	return isbn.replace(" ", "").replace("-", "");
}

public String getEditora() {
	return editora;
}

public String getCategoria() {
	return categoria;
}

public static int getQtd() {
	return qtd;
}

public String get_dados() {
		
	return "\nTítulo: " + this.titulo+
   "\nISBN: " + this.isbn+
   "\nEditora: " + this.editora+
   "\nCategoria: " + this.categoria;  
   

}

}