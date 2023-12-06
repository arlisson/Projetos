package TrabalhoController;


import java.time.LocalDate;
import java.util.List;

import TrabalhoDAO.*;
import TrabalhoModel.*;

public class EmprestimoController {
	
	
	private EmprestimoDAO emprestimodao = new EmprestimoDAO();
	
	
public boolean insert(Emprestimo emprestimo) {
		
	return emprestimodao.insert(emprestimo);				
}
	

	
public boolean update_prazo(int id) {
		return emprestimodao.update_prazo(id);
		
			
}
	
public List<Emprestimo> select_all() {
return emprestimodao.select_all();
	
	
}

public List<Emprestimo> join_isbn(String isbn) {
	return emprestimodao.join_isbn(isbn);

}


public List<Emprestimo> join_cpf(String cpf) {
	return emprestimodao.join_cpf(cpf);
}
	
public Emprestimo select_one_user(String cpf) {
	return emprestimodao.select_one_user(cpf);
	
}
public Emprestimo select_one_book(String isbn) {
	return emprestimodao.select_one_book(isbn);
	
}
public List<Emprestimo> select_abertos() {
	return emprestimodao.select_abertos();
	

}
public List<Emprestimo> select_atrasados() {
	return emprestimodao.select_atrasados();
	

}
public List<Emprestimo> select_finalizados() {
	return emprestimodao.select_finalizados();
	

}
public boolean update_data(int id) {
	return emprestimodao.update_data(id);
}
public boolean update_atraso(int id) {
	return emprestimodao.update_atraso(id);
}

public void atraso() {
	for(Emprestimo e:emprestimodao.select_all()) {
		if(LocalDate.parse(e.getPrazo()).compareTo(LocalDate.now())<0 && e.getData_entrega()==null) {
			emprestimodao.update_atraso(e.getId_emprestimo());
		}
	}
}
	
}
