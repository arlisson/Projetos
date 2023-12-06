package TrabalhoDAO;
import Trabalho.*;
import TrabalhoModel.Livro;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class LivroDAO {
	private Connection connection;
	private final String INSERT = "INSERT INTO livros (isbn,titulo,editora,categoria) VALUES (?,?,?,?)";
	private final String SELECT_ONE = "SELECT * FROM livros WHERE isbn = ?";
	private final String SELECT_TITULO = "SELECT * FROM livros WHERE titulo = ?";
	private final String SELECT_EDITORA = "SELECT * FROM livros WHERE editora = ?";
	private final String SELECT_CATIGURIA = "SELECT * FROM livros WHERE categoria = ?";
	
	public LivroDAO() {
		try {
			
			connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/biblioteca?user=root");
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
	}
	
	public boolean insert(Livro livro) {
		try {
			PreparedStatement ps = connection.prepareStatement(INSERT);
			ps.setString(1, livro.getIsbn());
			ps.setString(2, livro.getTitulo());
			ps.setString(3, livro.getEditora());
			ps.setString(4, livro.getCategoria());
			ps.execute();
			return true;
			
		} catch (SQLException e) {
			e.getStackTrace();
			return false;
		}
	}
	
	public boolean select_isbn(String isbn) {
		try {			
			PreparedStatement ps;
			ps = connection.prepareStatement(SELECT_ONE);
			ps.setString(1, isbn);
			ResultSet result =  ps.executeQuery();
			if (!result.next()) {
				return false;
			}
			
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return true;
	}
	
	public Livro select_isbntxt(String isbn) {
		try {		
			
			PreparedStatement ps;
			ps = connection.prepareStatement(SELECT_ONE);
			ps.setString(1, isbn);
			ResultSet result =  ps.executeQuery();
			if (!result.next()) {
				return null;
			}
			return new Livro(result.getString("titulo"),result.getString("isbn"),result.getString("editora"),result.getString("categoria"));
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return null;
		
	}
	public List<Livro> select_titulo(String titulo) {
		try {	
				
			List<Livro> livros = new ArrayList<>();
			PreparedStatement ps;
			ps = connection.prepareStatement(SELECT_TITULO);
			ps.setString(1, titulo);
			ResultSet result =  ps.executeQuery();
					
			while(result.next()) {
					livros.add(new Livro(result.getString("titulo"),result.getString("isbn"),result.getString("editora"),result.getString("categoria")));
				}			
			return livros;
				
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return null;
	}
	
	public List<Livro> select_editora(String editora) {
		try {	
				
			List<Livro> livros = new ArrayList<>();
			PreparedStatement ps;
			ps = connection.prepareStatement(SELECT_EDITORA);
			ps.setString(1, editora);
			ResultSet result =  ps.executeQuery();
					
			while(result.next()) {
					livros.add(new Livro(result.getString("titulo"),result.getString("isbn"),result.getString("editora"),result.getString("categoria")));
				}			
			return livros;
				
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return null;
	}
	public List<Livro> select_catiguria(String categoria) {
		try {	
				
			List<Livro> livros = new ArrayList<>();
			PreparedStatement ps;
			ps = connection.prepareStatement(SELECT_CATIGURIA);
			ps.setString(1, categoria);
			ResultSet result =  ps.executeQuery();
					
			while(result.next()) {
					livros.add(new Livro(result.getString("titulo"),result.getString("isbn"),result.getString("editora"),result.getString("categoria")));
				}			
			return livros;
				
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return null;
	}

}
