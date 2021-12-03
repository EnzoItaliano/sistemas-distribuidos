# Aluno: Enzo Dornelles Italiano - RA: 2044595
# Aluno: Lucas Henrique Malaquias da Silva Donadi - RA-1711598
# Descrição: código do cliente que envia as requisções e informações via TCP para um servidor que gerencia a aplicação.
# Data de criação: 18/11/2021.
# Atualizações: 19/11/2021, 20/11/2021, 21/11/2021, 22/11/2021.

import socket
import database_pb2

# menu da aplicação
def menu():
    print("---------------------------------")
    print("1-Inserir Matricula")
    print("2-Alteracao de notas")
    print("3-Alteracao de faltas")
    print("4-Listar alunos de uma disciplina")
    print("5-Boletim de aluno")
    print("6-Sair")
    msg = int(input("Escolha uma opcao:"))
    print("---------------------------------")
    return msg

if __name__ == '__main__':
    # conexao com servidor atraves de tcp
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 7000))
    
    msg = menu()

    while msg!=6:
        #Mensagem enviada
        #inputs de acordo com a ação selecionada no menu
        if msg == 1:
            client_socket.send(("1\n").encode('UTF-8'))
            matricula = database_pb2.Matricula()
            matricula.ra = int(input("RA:"));
            matricula.cod_disciplina = input("Codigo da disciplina:");
            matricula.ano = int(input("Ano:"));
            matricula.semestre = int(input("Semestre:"));

            msg_to_send = matricula.SerializeToString()
            size = len(msg_to_send)

            client_socket.send((str(size) + "\n").encode())
        elif msg == 2:
            client_socket.send(("2\n").encode('UTF-8'))
            matricula = database_pb2.Matricula()
            matricula.ra = int(input("RA:"));
            matricula.cod_disciplina = input("Codigo da disciplina:");
            matricula.ano = int(input("Ano:"));
            matricula.semestre = int(input("Semestre:"));
            matricula.nota = float(input("Nota:"));

            msg_to_send = matricula.SerializeToString()
            size = len(msg_to_send)

            client_socket.send((str(size) + "\n").encode())
        elif msg == 3:
            client_socket.send(("3\n").encode('UTF-8'))
            matricula = database_pb2.Matricula()
            matricula.ra = int(input("RA:"));
            matricula.cod_disciplina = input("Codigo da disciplina:");
            matricula.ano = int(input("Ano:"));
            matricula.semestre = int(input("Semestre:"));
            matricula.faltas = int(input("Faltas:"));

            msg_to_send = matricula.SerializeToString()
            size = len(msg_to_send)

            client_socket.send((str(size) + "\n").encode())
        elif msg == 4:
            client_socket.send(("4\n").encode('UTF-8'))
            matricula = database_pb2.Matricula()
            matricula.cod_disciplina = input("Codigo da disciplina:");
            matricula.ano = int(input("Ano:"));
            matricula.semestre = int(input("Semestre:"));

            msg_to_send = matricula.SerializeToString()
            size = len(msg_to_send)

            client_socket.send((str(size) + "\n").encode())
        elif msg == 5:
            client_socket.send(("5\n").encode('UTF-8'))
            matricula = database_pb2.Matricula()
            matricula.ra = int(input("RA:"));
            matricula.ano = int(input("Ano:"));
            matricula.semestre = int(input("Semestre:"));

            msg_to_send = matricula.SerializeToString()
            size = len(msg_to_send)

            client_socket.send((str(size) + "\n").encode())
        elif msg == 6: break
        client_socket.send(msg_to_send)

        #Mensagem recebida como resposta do servidor
        ans = client_socket.recv(1024)
        if msg != 4 and msg != 5:
            ans=ans.decode()
            print("\nServidor>> ", ans)
        else:
            ans=ans.decode().split("\n")
            print("\nServidor>> Resultados:", len(ans)-2)
            for x in ans[:-1]:
                print(x)

        msg = menu()
    client_socket.close()