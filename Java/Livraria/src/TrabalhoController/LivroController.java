package TrabalhoController;


import java.util.List;

import TrabalhoDAO.*;
import TrabalhoModel.*;
public class LivroController {
	
	
	LivroDAO livrodao = new LivroDAO();
	
public	static boolean verificaisbn(String isbn) {
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

public boolean insert(Livro livro) {
	return livrodao.insert(livro);
}

public boolean select_isbn(String isbn) {
	return livrodao.select_isbn(isbn);
}

public List<Livro> select_titulo (String titulo) {
	if(livrodao.select_titulo(titulo).isEmpty()) {
		return null;
	}
	return livrodao.select_titulo(titulo);
}
public Livro select_isbntxt(String isbn) {
	
	return livrodao.select_isbntxt(isbn);
	
}
public List<Livro> select_editora(String editora){
	return livrodao.select_editora(editora);
}
public List<Livro> select_catiguria(String categoria){
	return livrodao.select_catiguria(categoria);
}
	
}
