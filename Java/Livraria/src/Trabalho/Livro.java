package Trabalho;

public class Livro {

	private String titulo;
	private String isbn;
	private String editora;
	private String categoria;
	private static int qtd;
	




public Livro (String titulo, String isbn, String editora, String categoria) {
	
	this.titulo = titulo;
	this.editora = editora;
	this.categoria = categoria;	
	qtd++;
	verificaisbn(isbn);
	this.isbn = isbn.replace(" ", "").replace("-", "");
	
}

static boolean verificaisbn(String isbn) {
        // Remover espaços em branco e hifens do código ISBN
        isbn = isbn.replace(" ", "").replace("-", "");
        
        // Verificar se o ISBN possui 13 dígitos
        if (isbn.length() != 13) {
            return false;
        }
        
        // Calcular o dígito de verificação
        int sum = 0;
        for (int i = 0; i < 12; i++) {
            int digit = Character.getNumericValue(isbn.charAt(i));
            sum += (i % 2 == 0) ? digit : digit * 3;
        }
        int checkDigit = (10 - (sum % 10)) % 10;
        
        // Verificar se o dígito de verificação está correto
        int lastDigit = Character.getNumericValue(isbn.charAt(12));
        return checkDigit == lastDigit;
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
		
	return "Título: " + this.titulo+
   "\nISBN: " + this.isbn+
   "\nEditora: " + this.editora+
   "\nCategoria: " + this.categoria;  
   

}

}