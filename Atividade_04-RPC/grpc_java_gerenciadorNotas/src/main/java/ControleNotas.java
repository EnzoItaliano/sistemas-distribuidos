// Aluno: Enzo Dornelles Italiano - RA: 2044595
// Aluno: Lucas Henrique Malaquias da Silva Donadi - RA-1711598
// Descrição: código do servidor que gerencia matriculas de uma aplicação via comunicação gRPC.
// Data de criação: 26/11/2021.
// Atualizações: 28/11/2021, 02/12/2021, 03/12/2021.


import io.grpc.stub.StreamObserver;
import java.sql.*;

/**
 *
 * @author Enzo Italiano e Lucas Donadi
 */

public class ControleNotas extends ControleNotasGrpc.ControleNotasImplBase {
    // conecta com o banco de dados
    static final Connection connection = connect();

    // cria conexão com o banco de dados
    public static Connection connect() {
        Connection conn = null;

        try {
            // URL do banco de dados
            String url = "jdbc:sqlite:../database_com_dados-contrib-Daniel-Farina.db";

            // Colicita conexão com o banco de dados
            conn = DriverManager.getConnection(url);

        } catch (SQLException e) {
            // Mostra erro de conexao
            System.out.println(e.getMessage());
        }

        return conn;
    }

    // Metodo que adiciona matricula
    @Override
    public void adicionarMatricula(MatriculaRequest request, StreamObserver<MatriculaResponse> responseObserver) {
        // Cria objeto de resposta
        MatriculaResponse.Builder response = MatriculaResponse.newBuilder();

        try {
            // Valida informacoes da requisicao
            if (request.getCodDisciplina() == "") {
                throw new SQLException("Codigo de Disciplina invalido");
            } else if (request.getRa() < 0) {
                throw new SQLException("RA invalido\n");
            } else if (request.getRa() < 0) {
                throw new SQLException("Ano invalido\n");
            } else if (request.getSemestre() < 1) {
                throw new SQLException("Semestre invalido\n");
            }

            // Atribui informacoes da requisicao para variaveis
            int ra = request.getRa();
            int ano = request.getAno();
            int semestre = request.getSemestre();
            String cod_disciplina = request.getCodDisciplina();

            // Cria um statemente para execucao de queries
            Statement statement = connection.createStatement();

            // Verifica se o aluno existe no banco de dados
            ResultSet resultSet = statement.executeQuery("SELECT ra FROM aluno WHERE ra=" + ra);
            if (resultSet.isBeforeFirst()) {
                // Verifica se a disciplina existe no banco de dados
                resultSet = statement
                        .executeQuery("SELECT * FROM disciplina WHERE codigo='" + String.valueOf(cod_disciplina) + "'");
                if (resultSet.isBeforeFirst()) {
                    // Insere informacoes
                    statement.executeUpdate(
                            "INSERT INTO matricula (ra, cod_disciplina, ano, semestre, nota, faltas) VALUES (" + ra
                                    + ", '" + String.valueOf(cod_disciplina) + "', " + ano + ", " + semestre
                                    + ", 0, 0);");

                    // Procura pelas informacoes inseridas
                    resultSet = statement.executeQuery("SELECT * FROM matricula WHERE ra=" + request.getRa()
                            + " AND cod_disciplina='" + String.valueOf(request.getCodDisciplina()) + "' AND ano="
                            + request.getAno() + " AND semestre=" + request.getSemestre() + ";");
                    if (resultSet.isBeforeFirst()) {
                        while (resultSet.next()) {
                            // Atribui os resultados obtidos a variaveis
                            int raResult = resultSet.getInt("ra");
                            int anoResult = resultSet.getInt("ano");
                            int semestreResult = resultSet.getInt("semestre");
                            String codigoDisciplinaResult = resultSet.getString("cod_disciplina");
                            float notaResult = resultSet.getFloat("nota");
                            int faltasResult = resultSet.getInt("faltas");
                            // Adiciona informacoes na resposta
                            response.setRa(raResult).setAno(anoResult)
                                    .setSemestre(semestreResult).setCodDisciplina(codigoDisciplinaResult)
                                    .setNota(notaResult).setFaltas(faltasResult).build();
                        }
                    } else {
                        throw new SQLException("Erro na matricula");
                    }
                } else {
                    throw new SQLException("Disciplina nao existe");
                }
            } else {
                throw new SQLException("Aluno nao existe");
            }
        } catch (SQLException e) {
            response.setMensagem(e.getMessage());
        }
        // Envia resposta
        MatriculaResponse res = response.build();
        responseObserver.onNext(res);
        responseObserver.onCompleted();
    }

    // Metodo que altera nota
    @Override
    public void alterarNota(MatriculaRequest request, StreamObserver<MatriculaResponse> responseObserver) {
        // Cria objeto de resposta
        MatriculaResponse.Builder response = MatriculaResponse.newBuilder();

        try {
            // Valida informacoes da requisicao
            if (request.getCodDisciplina() == "") {
                throw new SQLException("Codigo de Disciplina invalido\n");
            } else if (request.getRa() < 1) {
                throw new SQLException("RA invalido\n");
            } else if (request.getAno() < 0) {
                throw new SQLException("Ano invalido\n");
            } else if (request.getSemestre() < 1) {
                throw new SQLException("Semestre invalido\n");
            } else if (request.getNota() < 0) {
                throw new SQLException("Nota invalida\n");
            }

            // Atribui informacoes da requisicao para variaveis
            int ra = request.getRa();
            int ano = request.getAno();
            int semestre = request.getSemestre();
            String cod_disciplina = request.getCodDisciplina();
            float nota = request.getNota();

            // Cria um statemente para execucao de queries
            Statement statement = connection.createStatement();

            // Verifica se a matricula existe no banco de dados
            ResultSet resultSet = statement
                    .executeQuery("SELECT * FROM Matricula WHERE ra=" + ra + " and cod_disciplina='"
                            + String.valueOf(cod_disciplina) + "' and ano=" + ano + " and semestre=" + semestre);
            if (resultSet.isBeforeFirst()) {
                // Atualiza nota
                statement.executeUpdate(
                        "UPDATE Matricula SET nota=" + nota + " WHERE cod_disciplina='" + String.valueOf(cod_disciplina)
                                + "' and ra=" + ra + " and ano=" + ano + " and semestre=" + semestre);

                // Busca a matricula no banco de dados
                resultSet = statement.executeQuery("SELECT * FROM Matricula WHERE ra=" + ra + " and cod_disciplina='"
                        + String.valueOf(cod_disciplina) + "' and ano=" + ano + " and semestre=" + semestre + ";");
                if (resultSet.isBeforeFirst()) {
                    while (resultSet.next()) {
                        // Atribui os resultados obtidos a variaveis
                        int raResult = resultSet.getInt("ra");
                        int anoResult = resultSet.getInt("ano");
                        int semestreResult = resultSet.getInt("semestre");
                        String codigoDisciplinaResult = resultSet.getString("cod_disciplina");
                        float notaResult = resultSet.getFloat("nota");
                        int faltasResult = resultSet.getInt("faltas");
                        // Adiciona informacoes na resposta
                        response.setRa(raResult).setAno(anoResult)
                                .setSemestre(semestreResult).setCodDisciplina(codigoDisciplinaResult)
                                .setNota(notaResult).setFaltas(faltasResult).build();
                    }
                } else {
                    throw new SQLException("Erro na matricula");
                }
            } else {
                throw new SQLException("Matricula nao existe");
            }
        } catch (SQLException e) {
            response.setMensagem(e.getMessage());
        }
        // Envia resposta
        MatriculaResponse res = response.build();
        responseObserver.onNext(res);
        responseObserver.onCompleted();
    }

    // Metodo que altera faltas
    @Override
    public void alterarFaltas(MatriculaRequest request, StreamObserver<MatriculaResponse> responseObserver) {
        // Cria objeto de resposta
        MatriculaResponse.Builder response = MatriculaResponse.newBuilder();

        try {
            // Valida informacoes da requisicao
            if (request.getCodDisciplina() == "") {
                throw new SQLException("Codigo de Disciplina invalido\n");
            } else if (request.getRa() < 1) {
                throw new SQLException("RA invalido\n");
            } else if (request.getAno() < 0) {
                throw new SQLException("Ano invalido\n");
            } else if (request.getSemestre() < 1) {
                throw new SQLException("Semestre invalido\n");
            } else if (request.getFaltas() < 0) {
                throw new SQLException("Nota invalida\n");
            }

            // Atribui informacoes da requisicao para variaveis
            int ra = request.getRa();
            int ano = request.getAno();
            int semestre = request.getSemestre();
            String cod_disciplina = request.getCodDisciplina();
            int faltas = request.getFaltas();

            // Cria um statemente para execucao de queries
            Statement statement = connection.createStatement();

            // Verifica se a matricula existe no banco de dados
            ResultSet resultSet = statement
                    .executeQuery("SELECT * FROM Matricula WHERE ra=" + ra + " AND cod_disciplina='"
                            + String.valueOf(cod_disciplina) + "' AND ano=" + ano + " AND semestre=" + semestre);
            if (resultSet.isBeforeFirst()) {
                // Atualiza faltas
                statement.executeUpdate(
                        "UPDATE Matricula SET faltas=" + faltas + " WHERE cod_disciplina='"
                                + String.valueOf(cod_disciplina) + "' AND ra=" + ra + " AND ano=" + ano
                                + " AND semestre=" + semestre);

                // Busca a matricula no banco de dados
                resultSet = statement.executeQuery("SELECT * FROM Matricula WHERE ra=" + ra + " AND cod_disciplina='"
                        + String.valueOf(cod_disciplina) + "' AND ano=" + ano + " AND semestre=" + semestre + ";");
                if (resultSet.isBeforeFirst()) {
                    while (resultSet.next()) {
                        // Atribui os resultados obtidos a variaveis
                        int raResult = resultSet.getInt("ra");
                        int anoResult = resultSet.getInt("ano");
                        int semestreResult = resultSet.getInt("semestre");
                        String codigoDisciplinaResult = resultSet.getString("cod_disciplina");
                        float notaResult = resultSet.getFloat("nota");
                        int faltasResult = resultSet.getInt("faltas");
                        // Adiciona informacoes na resposta
                        response.setRa(raResult).setAno(anoResult)
                                .setSemestre(semestreResult).setCodDisciplina(codigoDisciplinaResult)
                                .setNota(notaResult).setFaltas(faltasResult).build();
                    }
                }
            } else {
                throw new SQLException("Matricula nao existe");
            }
        } catch (SQLException e) {
            response.setMensagem(e.getMessage());
        }
        // Envia resposta
        MatriculaResponse res = response.build();
        responseObserver.onNext(res);
        responseObserver.onCompleted();
    }

    // Metodo que lista os alunos de uma disciplina
    @Override
    public void listarAlunos(ListarAlunosRequest request, StreamObserver<ListarAlunosResponse> responseObserver) {
        // Cria objeto de resposta
        ListarAlunosResponse.Builder response = ListarAlunosResponse.newBuilder();

        try {
            // Valida informacoes da requisicao
            if (request.getCodDisciplina() == "") {
                throw new SQLException("Codigo de Disciplina invalido\n");
            } else if (request.getAno() < 0) {
                throw new SQLException("Ano invalido\n");
            } else if (request.getSemestre() < 1) {
                throw new SQLException("Semestre invalido\n");
            }

            // Atribui informacoes da requisicao para variaveis
            int ano = request.getAno();
            int semestre = request.getSemestre();
            String cod_disciplina = request.getCodDisciplina();

            // Cria um statemente para execucao de queries
            Statement statement = connection.createStatement();

            // Verifica se a disciplina existe no banco de dados
            ResultSet resultSet = statement.executeQuery(
                    "SELECT codigo FROM disciplina WHERE codigo='" + String.valueOf(cod_disciplina) + "'");
            if (resultSet.isBeforeFirst()) {
                // Busca se os alunos da disciplina no banco de dados
                resultSet = statement.executeQuery(
                        "SELECT a.ra, a.nome, a.periodo FROM matricula as m, aluno as a WHERE m.cod_disciplina='"
                                + String.valueOf(cod_disciplina) + "' and m.ra=a.ra and m.ano=" + ano
                                + " and m.semestre=" + semestre);
                if (resultSet.isBeforeFirst()) {
                    while (resultSet.next()) {
                        // Atribui os resultados obtidos a variaveis
                        int ra = resultSet.getInt("ra");
                        String nome = resultSet.getString("nome");
                        int periodo = resultSet.getInt("periodo");
                        // Adiciona informacoes na resposta
                        response.addAlunos(ListarAlunosResponse.Aluno.newBuilder().setNome(nome).setRa(ra)
                                .setPeriodo(periodo).build());
                    }
                } else {
                    throw new SQLException("Nao ha alunos matriculados neste ano e semestre para esta disciplina");
                }
            } else {
                throw new SQLException("Disciplina nao existe");
            }
        } catch (SQLException e) {
            response.setMensagem(e.getMessage());
        }
        // Envia resposta
        ListarAlunosResponse res = response.build();
        responseObserver.onNext(res);
        responseObserver.onCompleted();
    }

    // Metodo que mostra o boletim de um aluno
    @Override
    public void listarDisciplinasAluno(BoletimRequest request, StreamObserver<BoletimResponse> responseObserver) {
        // Cria objeto de resposta
        BoletimResponse.Builder response = BoletimResponse.newBuilder();

        try {
            // Valida informacoes da requisicao
            if (request.getRa() < 0) {
                throw new SQLException("RA invalido\n");
            } else if (request.getAno() < 0) {
                throw new SQLException("Ano invalido\n");
            } else if (request.getSemestre() < 1) {
                throw new SQLException("Semestre invalido\n");
            }

            // Atribui informacoes da requisicao para variaveis
            int ra = request.getRa();
            int ano = request.getAno();
            int semestre = request.getSemestre();

            // Cria um statemente para execucao de queries
            Statement statement = connection.createStatement();

            // Verifica se o aluno existe no banco de dados
            ResultSet resultSet = statement.executeQuery("SELECT ra FROM aluno WHERE ra=" + ra);
            if (resultSet.isBeforeFirst()) {
                // Busca se as disciplina do aluno no banco de dados
                resultSet = statement.executeQuery(
                        "SELECT a.ra, a.nome, m.cod_disciplina, m.nota, m.faltas FROM matricula as m, aluno as a WHERE m.ra=a.ra and m.ra="
                                + ra + " and m.ano=" + ano + " and m.semestre=" + semestre);
                if (resultSet.isBeforeFirst()) {
                    while (resultSet.next()) {
                        // Atribui os resultados obtidos a variaveis
                        String codigoDisciplinaResult = resultSet.getString("cod_disciplina");
                        float nota = resultSet.getFloat("nota");
                        int faltas = resultSet.getInt("faltas");
                        // Adiciona informacoes na resposta
                        response.addDisciplinas(BoletimResponse.DisciplinaAlunos.newBuilder().setRa(request.getRa())
                                .setCodDisciplina(codigoDisciplinaResult).setNota(nota).setFaltas(faltas).build());
                    }
                } else {
                    throw new SQLException("Aluno não esta matriculado em nada neste ano e semestre");
                }
            } else {
                throw new SQLException("Aluno não existe");
            }
        } catch (SQLException e) {
            response.setMensagem(e.getMessage());
        }
        // Envia resposta
        BoletimResponse res = response.build();
        responseObserver.onNext(res);
        responseObserver.onCompleted();
    }

    // Metodo que mostra todas as disciplinas de um curso
    @Override
    public void listarDisciplinasCurso(ListarDisciplinasCursoRequest request,
            StreamObserver<ListarDisciplinasCursoResponse> responseObserver) {
        // Cria objeto de resposta
        ListarDisciplinasCursoResponse.Builder response = ListarDisciplinasCursoResponse.newBuilder();
        
        try {
            // Valida informacoes da requisicao
            if (request.getCodCurso() < 0) {
                throw new SQLException("Codigo do curso invalido\n");
            }

            // Atribui informacoes da requisicao para variaveis
            int cod_curso = request.getCodCurso();

            // Cria um statemente para execucao de queries
            Statement statement = connection.createStatement();

            // Busca nome do curso no banco de dados
            ResultSet resultSet = statement.executeQuery("SELECT nome FROM curso WHERE codigo=" + cod_curso);
            if (resultSet.isBeforeFirst()) {
                response.setNome(resultSet.getString("nome"));
            } else {
                throw new SQLException("O curso não existe");
            }

            // Busca as disciplina do curso no banco de dados
            resultSet = statement
                    .executeQuery("SELECT * FROM disciplina WHERE cod_curso=" + cod_curso);
            if (resultSet.isBeforeFirst()) {
                while (resultSet.next()) {
                    // Atribui os resultados obtidos a variaveis
                    String professor = resultSet.getString("professor");
                    String nome = resultSet.getString("nome");
                    String codigo = resultSet.getString("codigo");
                    // Adiciona informacoes na resposta
                    response.addDisciplinas(ListarDisciplinasCursoResponse.DisciplinaCurso.newBuilder().setNome(nome)
                            .setCodDisciplina(codigo).setProfessor(professor).build());
                }
            } else {
                throw new SQLException("O curso não possui nenhuma disciplina");
            }
        } catch (SQLException e) {
            response.setMensagem(e.getMessage());
        }
        // Envia resposta
        ListarDisciplinasCursoResponse res = response.build();
        responseObserver.onNext(res);
        responseObserver.onCompleted();
    }
}
