package TrabalhoController;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import TrabalhoDAO.*;
import TrabalhoModel.*;

public class UsuarioController {
	
	UsuarioDAO usuariodao = new UsuarioDAO();
	
public static boolean valida_cpf(String cpf) {
		
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
	
	
public boolean insert(Usuario usuario) {
	return usuariodao.insert(usuario);
	
}
public boolean select_cpf(String cpf) {
	return usuariodao.select_cpf(cpf);
}

public Usuario select_cpftxt(String cpf) {
	return usuariodao.select_cpftxt(cpf);
	
}
public List<Usuario> select_nome(String nome) {
	if(usuariodao.select_nome(nome).isEmpty()) {
		return null;
	}
	return usuariodao.select_nome(nome);
	
	}

}
