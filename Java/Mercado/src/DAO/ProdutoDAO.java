package DAO;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

import Model.Produto;

public class ProdutoDAO {
	
	private final static String SELECT_ALL = "SELECT * FROM produtos";
	private final static String INSERT = "INSERT INTO produtos (nome, preco) VALUES (?, ?)";
	private final static String SELECT_ID = "SELECT * FROM produtos WHERE id = ?";
	
    public static List<Produto> listarProdutos() {
        List<Produto> lista = new ArrayList<>();
        

        try (Connection conn = Database.connect();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(SELECT_ALL)) {

            while (rs.next()) {
                Produto p = new Produto(
                    rs.getInt("id"),
                    rs.getString("nome"),
                    rs.getDouble("preco")
                );
                lista.add(p);
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return lista;
    }
    
    public static void inserirProduto(String nome, double preco) {
        

        try (Connection conn = Database.connect();
             PreparedStatement stmt = conn.prepareStatement(INSERT)) {

            stmt.setString(1, nome);
            stmt.setDouble(2, preco);
            stmt.executeUpdate();

            System.out.println("Produto inserido com sucesso.");

        } catch (SQLException e) {
            System.out.println("Erro ao inserir produto: " + e.getMessage());
        }
    }
    
    public static Produto buscarProdutoId(int id) {
        try (Connection conn = Database.connect();
             PreparedStatement stmt = conn.prepareStatement(SELECT_ID)) {

            stmt.setInt(1, id);  

            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                Produto p = new Produto(
                    rs.getInt("id"),
                    rs.getString("nome"),
                    rs.getDouble("preco")
                );
               // System.out.println("Produto escolhido:\n" + p);
                return p;
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return null;
    }
}
