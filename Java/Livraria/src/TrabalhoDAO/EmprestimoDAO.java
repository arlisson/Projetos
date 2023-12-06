package TrabalhoDAO;


import Trabalho.*;
import TrabalhoDAO.*;
import TrabalhoController.*;
import TrabalhoModel.Emprestimo;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class EmprestimoDAO {
	private Connection connection;
	private final String INSERT = "INSERT INTO emprestimos (cpf_pessoa, isbn_livro, data_emprestimo,prazo) VALUES (?,?,?,?)";
	private LocalDate data = LocalDate.now() ;
	private final String SELECT_ONE_USER = "SELECT * FROM emprestimos WHERE cpf_pessoa = ? and (situacao = \"EM ABERTO\" OR situacao = \"ATRASADO\")";
	private final String SELECT_ONE_BOOK = "SELECT * FROM emprestimos WHERE isbn_livro = ? and (situacao = \"EM ABERTO\" OR situacao = \"ATRASADO\")";
	private final String UPDATE_PRAZO = "UPDATE emprestimos SET prazo=? WHERE id_emprestimo=?";
	private final String UPDATE_ENTREGA = "UPDATE emprestimos SET data_entrega=?,situacao = \"FINALIZADO\" WHERE id_emprestimo=?";
	private final String UPDATE_ATRASO = "UPDATE emprestimos SET situacao = \"ATRASADO\" WHERE id_emprestimo=?";
	private final String SELECT_ABERTOS = "SELECT * FROM emprestimos WHERE situacao = \"EM ABERTO\" OR situacao=\"ATRASADO\"";
	private final String SELECT_ATRASADOS= "SELECT * FROM emprestimos WHERE situacao = \"ATRASADO\"";
	private final String SELECT_FINALIZADOS= "SELECT * FROM emprestimos WHERE situacao = \"FINALIZADO\"";
	private final String JOIN = "SELECT e.*, p.nome AS nome_usuario, l.titulo AS titulo_livro\r\n"
			+ "FROM emprestimos e\r\n"
			+ "JOIN pessoas p ON e.cpf_pessoa = p.cpf\r\n"
			+ "JOIN livros l ON e.isbn_livro = l.isbn;\r\n";
			
	private final String JOIN_CPF = "SELECT e.*, p.nome AS nome_usuario, l.titulo AS titulo_livro\r\n"
			+ "FROM emprestimos e\r\n"
			+ "JOIN pessoas p ON e.cpf_pessoa = p.cpf\r\n"
			+ "JOIN livros l ON e.isbn_livro = l.isbn\r\n"
			+ "WHERE p.cpf = ?;\r\n";
	
	private final String JOIN_ISBN = "SELECT e.*, p.nome AS nome_usuario, l.titulo AS titulo_livro\r\n"
			+ "FROM emprestimos e\r\n"
			+ "JOIN pessoas p ON e.cpf_pessoa = p.cpf\r\n"
			+ "JOIN livros l ON e.isbn_livro = l.isbn\r\n"
			+ "WHERE l.isbn = ?;\r\n"
			+ "";

	UsuarioController usuariocontroller = new UsuarioController();
	LivroController livrocontroller = new LivroController();

	public EmprestimoDAO() {
		try {
		
			connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/biblioteca?user=root");
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
	
	public boolean insert(Emprestimo emprestimo) {
		
		try {
			PreparedStatement ps = connection.prepareStatement(INSERT);
			ps.setString(1, emprestimo.getUsuario().getCpf());
			ps.setString(2, emprestimo.getLivro().getIsbn());
			ps.setObject(3, data);
			ps.setObject(4, data.plusDays(7));
			ps.execute();
			return true;
		} catch (SQLException e) {
			e.getStackTrace();
			return false;
					
		}
			
	}
	
		
public boolean update_prazo(int id) {
		
		try {
			PreparedStatement ps = connection.prepareStatement(UPDATE_PRAZO);			
			ps.setObject(1, data.now().plusDays(14));
			ps.setObject(2, id);
			ps.execute();
			return true;
		} catch (SQLException e) {
			e.getStackTrace();
			return false;
					
		}
			
	}
public boolean update_atraso(int id) {
	
	try {
		PreparedStatement ps = connection.prepareStatement(UPDATE_ATRASO);	
		ps.setObject(1, id);
		ps.execute();
		return true;
	} catch (SQLException e) {
		e.getStackTrace();
		return false;
				
	}
		
}

public boolean update_data(int id) {
	
	try {
		PreparedStatement ps = connection.prepareStatement(UPDATE_ENTREGA);			
		ps.setObject(1, data.now());
		ps.setObject(2, id);
		ps.execute();
		return true;
	} catch (SQLException e) {
		e.getStackTrace();
		return false;
				
	}
		
}


public Emprestimo select_one_user(String cpf) {
	
	try {
		PreparedStatement ps = connection.prepareStatement(SELECT_ONE_USER);			
		ps.setObject(1, cpf);
		
		ps.execute();
		ResultSet result =  ps.executeQuery();
		if(!result.next()) {
			return null;
		}
		Emprestimo emprestimo = new Emprestimo(livrocontroller.select_isbntxt(result.getString("isbn_livro")),usuariocontroller.select_cpftxt(result.getString("cpf_pessoa")));
		emprestimo.setDate(result.getString("data_emprestimo"));
		emprestimo.setPrazo(result.getString("prazo"));	
		emprestimo.setData_entrega(result.getString("data_entrega"));	
		emprestimo.setSituacao(result.getString("situacao"));	
		emprestimo.setId_emprestimo(result.getInt("id_emprestimo"));	
		return emprestimo;
	} catch (SQLException e) {
		e.getStackTrace();		
				
	}
	return null;
}
public Emprestimo select_one_book(String isbn) {
	
	try {
		PreparedStatement ps = connection.prepareStatement(SELECT_ONE_BOOK);			
		ps.setObject(1, isbn);
		
		ps.execute();
		ResultSet result =  ps.executeQuery();
		if(!result.next()) {
			return null;
		}
		Emprestimo emprestimo = new Emprestimo(livrocontroller.select_isbntxt(result.getString("isbn_livro")),usuariocontroller.select_cpftxt(result.getString("cpf_pessoa")));
		emprestimo.setDate(result.getString("data_emprestimo"));
		emprestimo.setPrazo(result.getString("prazo"));	
		emprestimo.setData_entrega(result.getString("data_entrega"));	
		emprestimo.setSituacao(result.getString("situacao"));	
		emprestimo.setId_emprestimo(result.getInt("id_emprestimo"));	
		return emprestimo;
	} catch (SQLException e) {
		e.getStackTrace();		
				
	}
	return null;
}
	
public List<Emprestimo> select_all() {
	try {	
		
		List<Emprestimo> emprestimos = new ArrayList<>();
		PreparedStatement ps;
		ps = connection.prepareStatement(JOIN);		
		ResultSet result =  ps.executeQuery();
		while(result.next()) {
			Emprestimo emprestimo = new Emprestimo(livrocontroller.select_isbntxt(result.getString("isbn_livro")),usuariocontroller.select_cpftxt(result.getString("cpf_pessoa")));
			emprestimo.setDate(result.getString("data_emprestimo"));
			emprestimo.setPrazo(result.getString("prazo"));	
			emprestimo.setData_entrega(result.getString("data_entrega"));	
			emprestimo.setSituacao(result.getString("situacao"));	
			emprestimo.setId_emprestimo(result.getInt("id_emprestimo"));	
			emprestimos.add(emprestimo);
			
		}
		
	return emprestimos;
		
	} catch (SQLException e) {
		e.printStackTrace();
	}
	return null;
	
	
	}

public List<Emprestimo> join_isbn(String isbn) {
	try {		
		List<Emprestimo> emprestimos = new ArrayList<>();
		PreparedStatement ps;
		ps = connection.prepareStatement(JOIN_ISBN);
		ps.setString(1, isbn);
		ResultSet result =  ps.executeQuery();
		while (result.next()) {
			Emprestimo emprestimo = new Emprestimo(livrocontroller.select_isbntxt(result.getString("isbn_livro")),usuariocontroller.select_cpftxt(result.getString("cpf_pessoa")));
			emprestimo.setDate(result.getString("data_emprestimo"));
			emprestimo.setPrazo(result.getString("prazo"));
			emprestimo.setSituacao(result.getString("situacao"));
			emprestimo.setData_entrega(result.getString("data_entrega"));
			emprestimo.setId_emprestimo(result.getInt("id_emprestimo"));
			emprestimos.add(emprestimo);
		}
		
		
		
		return emprestimos;
		
		
	} catch (SQLException e) {
		e.printStackTrace();
	}
	return null;
}
public List<Emprestimo> join_cpf(String cpf) {
	try {		
		List<Emprestimo> emprestimos = new ArrayList<>();
		PreparedStatement ps;
		ps = connection.prepareStatement(JOIN_CPF);
		ps.setString(1, cpf);
		ResultSet result =  ps.executeQuery();
		while (result.next()) {
			Emprestimo emprestimo = new Emprestimo(livrocontroller.select_isbntxt(result.getString("isbn_livro")),usuariocontroller.select_cpftxt(result.getString("cpf_pessoa")));
			emprestimo.setDate(result.getString("data_emprestimo"));
			emprestimo.setPrazo(result.getString("prazo"));
			emprestimo.setSituacao(result.getString("situacao"));
			emprestimo.setData_entrega(result.getString("data_entrega"));
			emprestimo.setId_emprestimo(result.getInt("id_emprestimo"));
			emprestimos.add(emprestimo);
		}
		
		
		
		return emprestimos;
		
		
	} catch (SQLException e) {
		e.printStackTrace();
	}
	return null;
}

public List<Emprestimo> select_abertos() {
	try {	
		
		List<Emprestimo> emprestimos = new ArrayList<>();
		PreparedStatement ps;
		ps = connection.prepareStatement(SELECT_ABERTOS);		
		ResultSet result =  ps.executeQuery();
		while(result.next()) {
			Emprestimo emprestimo = new Emprestimo(livrocontroller.select_isbntxt(result.getString("isbn_livro")),usuariocontroller.select_cpftxt(result.getString("cpf_pessoa")));
			emprestimo.setDate(result.getString("data_emprestimo"));
			emprestimo.setPrazo(result.getString("prazo"));	
			emprestimo.setData_entrega(result.getString("data_entrega"));	
			emprestimo.setSituacao(result.getString("situacao"));	
			emprestimo.setId_emprestimo(result.getInt("id_emprestimo"));	
			emprestimos.add(emprestimo);
			
		}
		
	return emprestimos;
		
	} catch (SQLException e) {
		e.printStackTrace();
	}
	return null;
	
	
	}
public List<Emprestimo> select_atrasados() {
	try {	
		
		List<Emprestimo> emprestimos = new ArrayList<>();
		PreparedStatement ps;
		ps = connection.prepareStatement(SELECT_ATRASADOS);		
		ResultSet result =  ps.executeQuery();
		while(result.next()) {
			Emprestimo emprestimo = new Emprestimo(livrocontroller.select_isbntxt(result.getString("isbn_livro")),usuariocontroller.select_cpftxt(result.getString("cpf_pessoa")));
			emprestimo.setDate(result.getString("data_emprestimo"));
			emprestimo.setPrazo(result.getString("prazo"));	
			emprestimo.setData_entrega(result.getString("data_entrega"));	
			emprestimo.setSituacao(result.getString("situacao"));	
			emprestimo.setId_emprestimo(result.getInt("id_emprestimo"));	
			emprestimos.add(emprestimo);
			
		}
		
	return emprestimos;
		
	} catch (SQLException e) {
		e.printStackTrace();
	}
	return null;
	
	
	}
public List<Emprestimo> select_finalizados() {
	try {	
		
		List<Emprestimo> emprestimos = new ArrayList<>();
		PreparedStatement ps;
		ps = connection.prepareStatement(SELECT_FINALIZADOS);		
		ResultSet result =  ps.executeQuery();
		while(result.next()) {
			Emprestimo emprestimo = new Emprestimo(livrocontroller.select_isbntxt(result.getString("isbn_livro")),usuariocontroller.select_cpftxt(result.getString("cpf_pessoa")));
			emprestimo.setDate(result.getString("data_emprestimo"));
			emprestimo.setPrazo(result.getString("prazo"));	
			emprestimo.setData_entrega(result.getString("data_entrega"));	
			emprestimo.setSituacao(result.getString("situacao"));	
			emprestimo.setId_emprestimo(result.getInt("id_emprestimo"));	
			emprestimos.add(emprestimo);
			
		}
		
	return emprestimos;
		
	} catch (SQLException e) {
		e.printStackTrace();
	}
	return null;
	
	
	}

}
