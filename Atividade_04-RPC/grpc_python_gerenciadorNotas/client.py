# Aluno: Enzo Dornelles Italiano - RA: 2044595
# Aluno: Lucas Henrique Malaquias da Silva Donadi - RA-1711598
# Descrição: código do cliente que envia as requisições e informações via gRPC para um servidor que gerencia a aplicação.
# Data de criação: 26/11/2021.
# Atualizações: 28/11/2021, 02/12/2021, 03/12/2021.

import grpc

import service_pb2_grpc
import service_pb2

channel = grpc.insecure_channel('localhost:7778')
stub = service_pb2_grpc.ControleNotasStub(channel)

# Menu de opcoes
def menu():
    print("---------------------------------")
    print("1-Inserir Matricula")
    print("2-Alteracao de notas")
    print("3-Alteracao de faltas")
    print("4-Listar alunos de uma disciplina")
    print("5-Boletim de aluno")
    print("6-Listar disciplinas de um curso")
    print("7-Sair")
    msg = int(input("Escolha uma opcao:"))
    print("---------------------------------")
    return msg


def client():
    msg = menu()

    while msg != 7:

        # Opcao de inserir matricula
        if msg == 1:
            request = service_pb2.MatriculaRequest()
            # Recolhe informações para a requisição
            request.ra = int(input("RA:"))
            request.cod_disciplina = input("Codigo da disciplina:")
            request.ano = int(input("Ano:"))
            request.semestre = int(input("Semestre:"))
            # Envia requisicao
            response = stub.AdicionarMatricula(request)
            if response.mensagem == "":
                # Mostra os resultados obtidos
                print("\n>>Inserido: \nRA:{}\nCod_Disciplina:{}\nAno:{}\nSemestre:{}\nNota:{}\nFaltas:{}".format(
                    response.ra, response.cod_disciplina, response.ano, response.semestre, response.nota, response.faltas))
            else:
                # Mostra erros
                print(response.mensagem)
        # Opcao de alterar nota
        elif msg == 2:
            request = service_pb2.MatriculaRequest()
            # Recolhe informações para a requisição
            request.ra = int(input("RA:"))
            request.cod_disciplina = input("Codigo da disciplina:")
            request.ano = int(input("Ano:"))
            request.semestre = int(input("Semestre:"))
            request.nota = float(input("Nota:"))
            # Envia requisicao
            response = stub.AlterarNota(request)
            if response.mensagem == "":
                # Mostra os resultados obtidos
                print("\n>>Nota atualizada: \nRA:{}\nCod_Disciplina:{}\nAno:{}\nSemestre:{}\nNota:{}\nFaltas:{}".format(
                    response.ra, response.cod_disciplina, response.ano, response.semestre, response.nota, response.faltas))
            else:
                # Mostra erros
                print(response.mensagem)
        # Opcao de alterar faltas
        elif msg == 3:
            request = service_pb2.MatriculaRequest()
            # Recolhe informações para a requisição
            request.ra = int(input("RA:"))
            request.cod_disciplina = input("Codigo da disciplina:")
            request.ano = int(input("Ano:"))
            request.semestre = int(input("Semestre:"))
            request.faltas = int(input("Faltas:"))
            # Envia requisicao
            response = stub.AlterarFaltas(request)
            if response.mensagem == "":
                # Mostra os resultados obtidos
                print("\n>>Faltas atualizadas: \nRA:{}\nCod_Disciplina:{}\nAno:{}\nSemestre:{}\nNota:{}\nFaltas:{}".format(
                    response.ra, response.cod_disciplina, response.ano, response.semestre, response.nota, response.faltas))
            else:
                # Mostra erros
                print(response.mensagem)
        # Opcao que lista alunos de uma disciplina
        elif msg == 4:
            request = service_pb2.ListarAlunosRequest()
            # Recolhe informações para a requisição
            request.cod_disciplina = input("Codigo da disciplina:")
            request.ano = int(input("Ano:"))
            request.semestre = int(input("Semestre:"))
            # Envia requisicao
            response = stub.ListarAlunos(request)
            if response.mensagem == "":
                # Mostra os resultados obtidos
                print("\n>>Alunos da disciplina:")
                for aluno in response.alunos:
                    print(aluno)
            else:
                # Mostra erros
                print(response.mensagem)
        # Opcao que mostra boletim de um aluno em certo semestre e ano
        elif msg == 5:
            request = service_pb2.BoletimRequest()
            # Recolhe informações para a requisição
            request.ra = int(input("RA:"))
            request.ano = int(input("Ano:"))
            request.semestre = int(input("Semestre:"))
            # Envia requisicao
            response = stub.ListarDisciplinasAluno(request)
            if response.mensagem == "":
                # Mostra os resultados obtidos
                print("\n>>Boletim:")
                for i in range(len(response.disciplinas)):
                    print("Ra: " + str(response.disciplinas[i].ra) + "\nCódigo da Disciplina: " + str(response.disciplinas[i].cod_disciplina) + "\nNota: " + str(
                        response.disciplinas[i].nota) + "\nFaltas: " + str(response.disciplinas[i].faltas))
            else:
                # Mostra erros
                print(response.mensagem)
        # Opcao que mostra disciplinas de um curso
        elif msg == 6:
            request = service_pb2.ListarDisciplinasCursoRequest()
            # Recolhe informações para a requisição
            request.cod_curso = int(input("Digite o código do curso: "))
            # Envia requisicao
            response = stub.ListarDisciplinasCurso(request)
            if response.mensagem == "":
                # Mostra os resultados obtidos
                print("\n>>Disciplinas de {}".format(response.nome))
                for i in range(len(response.disciplinas)):
                    print("Código da Disciplina: " + str(response.disciplinas[i].cod_disciplina) + "\nNome: " + str(
                        response.disciplinas[i].nome) + "\nProfessor: " + str(response.disciplinas[i].professor))
            else:
                # Mostra erros
                print(response.mensagem)
        # Caso o usuario digite uma opcao inexistente
        else:
            print("Opção inválida")

        msg = menu()


if __name__ == '__main__':
    client()
