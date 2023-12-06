package TrabalhoDAO;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import Trabalho.*;
import TrabalhoModel.Usuario;
public class UsuarioDAO {
	private Connection connection;
	private final String INSERT = "INSERT INTO pessoas (cpf,nome,endereco) VALUES (?,?,?)";
	private final String SELECT_ONE = "SELECT * FROM pessoas WHERE cpf = ?";
	private final String SELECT_NOME = "SELECT * FROM pessoas WHERE nome = ?";
	
	public UsuarioDAO() {
		try {
		
			connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/biblioteca?user=root");
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
	
	public boolean insert(Usuario usuario) {
		try {
			PreparedStatement ps = connection.prepareStatement(INSERT);
			ps.setString(1, usuario.getCpf());
			ps.setString(2, usuario.getNome());
			ps.setString(3, usuario.getEndereco());
			ps.execute();
			return true;
		} catch (SQLException e) {
			e.getStackTrace();
			return false;			
		}
		
	}
	public boolean select_cpf(String cpf) {
		try {			
			PreparedStatement ps;
			ps = connection.prepareStatement(SELECT_ONE);
			ps.setString(1, cpf);
			ResultSet result =  ps.executeQuery();
			if (!result.next()) {
				return false;
			}
			
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		return true;
	}
	
	public Usuario select_cpftxt(String cpf) {
		try {		
			
			PreparedStatement ps;
			ps = connection.prepareStatement(SELECT_ONE);
			ps.setString(1, cpf);
			ResultSet result =  ps.executeQuery();
			if (!result.next()) {
				return null;
			}
			return new Usuario(result.getString("nome"),result.getString("cpf"),result.getString("endereco"));
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return null;
		
	}
	public List<Usuario> select_nome(String nome) {
		try {	
			
			List<Usuario> usuarios = new ArrayList<>();
			PreparedStatement ps;
			ps = connection.prepareStatement(SELECT_NOME);
			ps.setString(1, nome);
			ResultSet result =  ps.executeQuery();
			while(result.next()) {
				usuarios.add(new Usuario(result.getString("nome"),result.getString("cpf"),result.getString("endereco")));
			}			
			return usuarios;

		} catch (SQLException e) {
			e.printStackTrace();
		}
		return null;
	}
	
	
}
