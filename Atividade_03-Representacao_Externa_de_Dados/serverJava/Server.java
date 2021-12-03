// Aluno: Enzo Dornelles Italiano - RA: 2044595
// Aluno: Lucas Henrique Malaquias da Silva Donadi - RA-1711598
// Descrição: código do servidor que gerencia a aplicação e recebe as requisções e informações via TCP.
// Data de criação: 18/11/2021.
// Atualizações: 19/11/2021, 20/11/2021, 21/11/2021, 22/11/2021.

import java.net.*;
import java.io.*;
import java.sql.*;

public class Server {
    static Connection db_connection;
   
    public static void main(String args[]) {
        try {
            // Conexao com banco de dados
            db_connection = SQLiteJDBCDriverConnection.connect();

            int serverPort = 7000; 
            // listen port
            ServerSocket listenSocket = new ServerSocket(serverPort);
            while (true) {
                // socket accept
                Socket clientSocket = listenSocket.accept();
                
                /* cria um thread para atender a conexao */
                ClientMessages c = new ClientMessages(clientSocket, db_connection);

                /* inicializa a thread */
                c.start();
            }
        } catch (IOException e) {
            System.out.println("Listen socket:" + e.getMessage());
        } 
    }
}

class ClientMessages extends Thread {
    DataInputStream inClient;
    DataOutputStream outClient;
    Socket clientSocket;
    Connection db_connection;

    public ClientMessages(Socket clientSocket, Connection db_connection) {
        try {
            this.clientSocket = clientSocket;
            this.db_connection = db_connection;
            inClient = new DataInputStream(clientSocket.getInputStream());
            outClient = new DataOutputStream(clientSocket.getOutputStream());
        } catch (IOException ioe) {
            System.out.println("Connection:" + ioe.getMessage());
        }
    }

    public void run() {
        while (true) {
            try {
                String typeOp = inClient.readLine();
                String decoded = new String(typeOp.getBytes("UTF-8"));
                Integer op = Integer.parseInt(decoded);
                
                if (op == 1) {
                    String valueStr = inClient.readLine();
                    int sizeBuffer = Integer.valueOf(valueStr);
                    byte[] buffer = new byte[sizeBuffer];
                    inClient.read(buffer);

                    Database.Matricula m = Database.Matricula.parseFrom(buffer);
                    System.out.println("--\n" + m + "--\n");
                    
                    String errors = "";
                    if(m.getCodDisciplina() == ""){
                        System.out.println("Codigo de Disciplina invalido\n");
                        errors += "Codigo de Disciplina invalido\n";
                    }
                    else if(m.getRa() < 1){
                        System.out.println("RA invalido\n");
                        errors += "RA invalido\n";
                    }
                    else if(m.getAno() < 0){
                        System.out.println("Ano invalido\n");
                        errors += "Ano invalido\n";
                    }
                    else if(m.getSemestre() < 1){
                        System.out.println("Semestre invalido\n");
                        errors += "Semestre invalido\n";
                    }

                    if(errors != ""){
                        outClient.write(errors.getBytes());
                        continue;
                    }

                    Integer ra = m.getRa();
                    String cod_disciplina = m.getCodDisciplina();
                    Integer ano = m.getAno();
                    Integer semestre = m.getSemestre();

                    try {
                        Statement statement = db_connection.createStatement();
                        ResultSet resultSet = statement.executeQuery("SELECT ra FROM aluno WHERE ra="+ra);
                        if(resultSet.isBeforeFirst()){
                            resultSet = statement.executeQuery("SELECT codigo FROM disciplina WHERE codigo='"+cod_disciplina+"'");
                            if(resultSet.isBeforeFirst()){
                                statement.executeUpdate("INSERT INTO matricula( ra, cod_disciplina, ano, semestre, nota, faltas) VALUES ( "+ra+", '"+cod_disciplina+"', "+ano+", "+semestre+", 0.0, 0)");
                                byte[] bytes = ("Matricula inserida:\nRA:"+ra+"\nCodigo da disciplina:"+cod_disciplina+"\nAno:"+ano+"\nSemestre:"+semestre+"\nNota:0.0\nFaltas:0").getBytes();
                                outClient.write(bytes);
                            }else{
                                System.out.println("Disciplina nao existe");
                                outClient.write(("Disciplina nao existe").getBytes());
                            }
                        }else{
                            System.out.println("Aluno nao existe");
                            outClient.write(("Aluno nao existe").getBytes());
                        }

                    } catch (SQLException e) {
                        System.out.println(e);
                    }
                } // If 1
                else if (op == 2) {
                    String valueStr = inClient.readLine();
                    int sizeBuffer = Integer.valueOf(valueStr);
                    byte[] buffer = new byte[sizeBuffer];
                    inClient.read(buffer);

                    Database.Matricula m = Database.Matricula.parseFrom(buffer);
                    System.out.println("--\n" + m + "--\n");
                    
                    String errors = "";
                    if(m.getCodDisciplina() == ""){
                        System.out.println("Codigo de Disciplina invalido\n");
                        errors += "Codigo de Disciplina invalido\n";
                    }
                    else if(m.getRa() < 1){
                        System.out.println("RA invalido\n");
                        errors += "RA invalido\n";
                    }
                    else if(m.getAno() < 0){
                        System.out.println("Ano invalido\n");
                        errors += "Ano invalido\n";
                    }
                    else if(m.getSemestre() < 1){
                        System.out.println("Semestre invalido\n");
                        errors += "Semestre invalido\n";
                    }
                    else if(m.getNota() < 0){
                        System.out.println("Nota invalida\n");
                        errors += "Nota invalida\n";
                    }

                    if(errors != ""){
                        outClient.write(errors.getBytes());
                        continue;
                    }

                    Integer ra = m.getRa();
                    String cod_disciplina = m.getCodDisciplina();
                    Integer ano = m.getAno();
                    Integer semestre = m.getSemestre();
                    Float nota = m.getNota();

                    try {
                        Statement statement = db_connection.createStatement();
                        ResultSet resultSet = statement.executeQuery("SELECT ra FROM aluno WHERE ra="+ra);
                        
                        if(resultSet.isBeforeFirst()){
                            resultSet = statement.executeQuery("SELECT codigo FROM disciplina WHERE codigo='"+cod_disciplina+"'");
                            if(resultSet.isBeforeFirst()){
                                statement.execute("UPDATE matricula SET nota="+nota+" WHERE cod_disciplina='"+cod_disciplina+"' and ra="+ra+" and ano="+ano+" and semestre="+semestre);
                                resultSet = statement.executeQuery("SELECT * FROM matricula WHERE cod_disciplina='"+cod_disciplina+"' and ra="+ra+" and ano="+ano+" and semestre="+semestre);
                                byte[] bytes = ("Nota atualizada:\nRA:"+resultSet.getInt("ra")+"\nCodigo da disciplina:"+resultSet.getString("cod_disciplina")+"\nAno:"+resultSet.getInt("ano")+"\nSemestre:"+resultSet.getInt("semestre")+"\nNota:"+resultSet.getFloat("nota")+"\nFaltas:"+resultSet.getInt("faltas")).getBytes();
                                outClient.write(bytes);
                            }else{
                                System.out.println("Disciplina nao existe");
                                outClient.write(("Disciplina nao existe").getBytes());
                            }
                        }else{
                            System.out.println("Aluno nao existe");
                            outClient.write(("Aluno nao existe").getBytes());
                        }

                    } // Try
                    catch (SQLException e) {
                        System.out.println(e);
                    } // Catch
                } // Else if 2
                else if (op == 3) {
                    String valueStr = inClient.readLine();
                    int sizeBuffer = Integer.valueOf(valueStr);
                    byte[] buffer = new byte[sizeBuffer];
                    inClient.read(buffer);

                    Database.Matricula m = Database.Matricula.parseFrom(buffer);
                    System.out.println("--\n" + m + "--\n");
                    
                    String errors = "";
                    if(m.getRa() < 1){
                        System.out.println("RA invalido\n");
                        errors += "RA invalido\n";
                    }
                    else if(m.getCodDisciplina() == ""){
                        System.out.println("Codigo de Disciplina invalido\n");
                        errors += "Codigo de Disciplina invalido\n";
                    } 
                    else if(m.getAno() < 0){
                        System.out.println("Ano invalido\n");
                        errors += "Ano invalido\n";
                    }
                    else if(m.getSemestre() < 1){
                        System.out.println("Semestre invalido\n");
                        errors += "Semestre invalido\n";
                    }
                    else if(m.getFaltas() < 0){
                        System.out.println("Faltas invalidas\n");
                        errors += "Faltas invalidas\n";
                    }

                    if(errors != ""){
                        outClient.write(errors.getBytes());
                        continue;
                    }

                    Integer ra = m.getRa();
                    String cod_disciplina = m.getCodDisciplina();
                    Integer ano = m.getAno();
                    Integer semestre = m.getSemestre();
                    Integer faltas = m.getFaltas();

                    try {
                        Statement statement = db_connection.createStatement();
                        ResultSet resultSet = statement.executeQuery("SELECT ra FROM aluno WHERE ra="+ra);
                        
                        if(resultSet.isBeforeFirst()){
                            resultSet = statement.executeQuery("SELECT codigo FROM disciplina WHERE codigo='"+cod_disciplina+"'");
                            if(resultSet.isBeforeFirst()){
                                statement.execute("UPDATE matricula SET faltas="+faltas+" WHERE cod_disciplina='"+cod_disciplina+"' and ra="+ra+" and ano="+ano+" and semestre="+semestre);
                                resultSet = statement.executeQuery("SELECT * FROM matricula WHERE cod_disciplina='"+cod_disciplina+"' and ra="+ra+" and ano="+ano+" and semestre="+semestre);
                                byte[] bytes = ("Nota atualizada:\nRA:"+resultSet.getInt("ra")+"\nCodigo da disciplina:"+resultSet.getString("cod_disciplina")+"\nAno:"+resultSet.getInt("ano")+"\nSemestre:"+resultSet.getInt("semestre")+"\nNota:"+resultSet.getFloat("nota")+"\nFaltas:"+resultSet.getInt("faltas")).getBytes();
                                outClient.write(bytes);
                            }else{
                                System.out.println("Disciplina nao existe");
                                outClient.write(("Disciplina nao existe").getBytes());
                            }
                        }else{
                            System.out.println("Aluno nao existe");
                            outClient.write(("Aluno nao existe").getBytes());
                        }

                    } // Try
                    catch (SQLException e) {
                        System.out.println(e);
                    } // Catch
                } // Else if 3
                else if (op == 4) {
                    String valueStr = inClient.readLine();
                    int sizeBuffer = Integer.valueOf(valueStr);
                    byte[] buffer = new byte[sizeBuffer];
                    inClient.read(buffer);

                    Database.Matricula m = Database.Matricula.parseFrom(buffer);
                    System.out.println("--\n" + m + "--\n");
                    
                    String errors = "";
                    if(m.getCodDisciplina() == ""){
                        System.out.println("Codigo de Disciplina invalido\n");
                        errors += "Codigo de Disciplina invalido\n";
                    }
                    else if(m.getAno() < 0){
                        System.out.println("Ano invalido\n");
                        errors += "Ano invalido\n";
                    }
                    else if(m.getSemestre() < 1){
                        System.out.println("Semestre invalido\n");
                        errors += "Semestre invalido\n";
                    }

                    if(errors != ""){
                        outClient.write(errors.getBytes());
                        continue;
                    }

                    String cod_disciplina = m.getCodDisciplina();
                    Integer ano = m.getAno();
                    Integer semestre = m.getSemestre();

                    try {
                        Statement statement = db_connection.createStatement();
                        ResultSet resultSet = statement.executeQuery("SELECT codigo FROM disciplina WHERE codigo='"+cod_disciplina+"'");
                        
                        if(resultSet.isBeforeFirst()){
                            resultSet = statement.executeQuery("SELECT a.ra, a.nome, a.periodo FROM matricula as m, aluno as a WHERE m.cod_disciplina='"+cod_disciplina+"' and m.ra=a.ra");
                            String bigArray = "RA\tNOME\tPERIODO\n";
                            while (resultSet.next()) {
                                Integer ra = resultSet.getInt("ra");
                                String nome = resultSet.getString("nome");
                                Integer periodo = resultSet.getInt("periodo");
                                
                                bigArray += ""+ra+"\t"+nome+"\t"+periodo+"\n";
                            }
                            outClient.write(bigArray.getBytes());
                        }else{
                            System.out.println("Disciplina nao existe");
                            outClient.write(("Disciplina nao existe").getBytes());
                        }

                    } // Try
                    catch (SQLException e) {
                        System.out.println(e);
                    } // Catch
                } // Else if 4
                else if (op == 5) {
                    String valueStr = inClient.readLine();
                    int sizeBuffer = Integer.valueOf(valueStr);
                    byte[] buffer = new byte[sizeBuffer];
                    inClient.read(buffer);

                    Database.Matricula m = Database.Matricula.parseFrom(buffer);
                    System.out.println("--\n" + m + "--\n");
                    
                    String errors = "";
                    if(m.getRa() < 1){
                        System.out.println("RA invalido\n");
                        errors += "RA invalido\n";
                    }
                    else if(m.getAno() < 0){
                        System.out.println("Ano invalido\n");
                        errors += "Ano invalido\n";
                    }
                    else if(m.getSemestre() < 1){
                        System.out.println("Semestre invalido\n");
                        errors += "Semestre invalido\n";
                    }

                    if(errors != ""){
                        outClient.write(errors.getBytes());
                        continue;
                    }

                    Integer ra = m.getRa();
                    Integer ano = m.getAno();
                    Integer semestre = m.getSemestre();

                    try {
                        Statement statement = db_connection.createStatement();
                        ResultSet resultSet = statement.executeQuery("SELECT ra FROM aluno WHERE ra="+ra);
                        if(resultSet.isBeforeFirst()){
                            ResultSet rs = statement.executeQuery("SELECT a.ra, a.nome, m.cod_disciplina, m.nota, m.faltas FROM matricula as m, aluno as a WHERE m.ra=a.ra and m.ra="+ra+" and m.ano="+ano+" and m.semestre="+semestre);
                            String bigArray = "RA\tNOME\tCOD_DISCIPLINA\tNOTA\tFALTAS\n";
                            while (rs.next()) {
                                Integer ra_res = resultSet.getInt("ra");
                                String nome = resultSet.getString("nome");
                                String cod_disciplina = resultSet.getString("cod_disciplina");
                                Float nota = resultSet.getFloat("nota");
                                Integer faltas = resultSet.getInt("faltas");
                                
                                bigArray += ""+ra_res+"\t"+nome+"\t"+cod_disciplina+"\t\t"+nota+"\t"+faltas+"\n";
                            }
                            System.out.println(bigArray);
                            outClient.write(bigArray.getBytes());
                        }else{
                            System.out.println("Disciplina nao existe");
                            outClient.write(("Disciplina nao existe").getBytes());
                        }

                    } // Try
                    catch (SQLException e) {
                        System.out.println(e);
                    } // Catch
                } // Else if 5
                else if (op == 6) {
                    break;
                } // Else if 6
                else {
                    outClient.write(("Digite uma opção válida").getBytes());
                }
            } // Try
            catch (IOException e) {

            }
        }
    }
}