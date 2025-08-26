package DAO;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Database {
    // Caminho do banco de dados SQLite (cria o arquivo se não existir)
	private static final String URL = "jdbc:sqlite:mercado.db";

    // Método para obter a conexão
    public static Connection connect() throws SQLException {
        return DriverManager.getConnection(URL);
    }

    // Método para testar a conexão
    public static void main(String[] args) {
        try (Connection conn = connect()) {
            if (conn != null) {
                System.out.println("Conexão com SQLite estabelecida com sucesso.");
            }
        } catch (SQLException e) {
            System.out.println("Erro ao conectar com SQLite: " + e.getMessage());
        }
    }
}
