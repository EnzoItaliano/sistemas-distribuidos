import java.sql.*;

public class SQLiteJDBCDriverConnection {

    public static Connection connect() {
        try {
            Connection connection = DriverManager.getConnection("jdbc:sqlite:../database/database_com_dados-contrib-Daniel-Farina.db");
            System.out.println("Conexão realizada !!!!");
            return connection;
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
        return null;
    }

    public static void main(String[] args) {
        connect();
    }
}