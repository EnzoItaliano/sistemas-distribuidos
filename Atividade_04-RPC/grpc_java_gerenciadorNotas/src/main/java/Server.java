// Aluno: Enzo Dornelles Italiano - RA: 2044595
// Aluno: Lucas Henrique Malaquias da Silva Donadi - RA-1711598
// Descrição: código do servidor que gerencia matriculas de uma aplicação via comunicação gRPC.
// Data de criação: 26/11/2021.
// Atualizações: 28/11/2021, 02/12/2021, 03/12/2021.

import io.grpc.ServerBuilder;
import java.io.IOException;

/**
 *
 * @author Henrique Moura Bini e Vinicius Henrique Soares
 */
public class Server {
    public static void main(String[] args) {
            io.grpc.Server server = ServerBuilder
                    .forPort(7778)
                    .addService(new ControleNotas())
                    .build();
            
            
        try {
            server.start();
            System.out.println("Servidor iniciado.");
            server.awaitTermination();
        } catch (IOException | InterruptedException e) {
            System.err.println("Erro: " + e);
        }
        
    }
}
