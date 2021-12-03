# Aluno: Enzo Dornelles Italiano - RA: 2044595
# Aluno: Lucas Henrique Malaquias da Silva Donadi - RA: 1711598
# Descrição: código do servidor para comunicação TCP para questão 1.
# Data de criação: 15/10/2021.
# Atualizações: 16/10/2021, 18/10/2021, 22/10/2021, 24/10/2021.

import socket
import _thread
import os
import hashlib
import sys

HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

USERS = [
    {
        'id': 1,
        'name': 'enzo',
        'password': '123'
    },
    {
        'id': 2,
        'name': 'admin',
        'password': 'admin'
    },
    {
        'id': 3,
        'name': 'teste',
        'password': 'teste'
    }
]

def msgProcessing(msg):
    msg = msg.decode('utf-8')
    return msg.split()

def conectado(con, cliente):
    print('Conectado por', cliente)
    auth = False
    folder = ''
    while True:
        msg = con.recv(1024)
        if not msg: break

        n_msg = msgProcessing(msg)

        if n_msg[0] == 'CONNECT':
            for user in USERS:
                if user['name'] == n_msg[1][:-1] and hashlib.sha512( user['password'].encode("utf-8") ).hexdigest() == n_msg[2]:
                    auth = True
                    folder = f'./client{user["id"]}'
                    os.chdir(folder)
                    print('SUCCESS')
                    con.send(b'SUCCESS')
            if auth == False:
                print('ERROR')
                con.send(b'ERROR')
        elif n_msg[0] == 'PWD' and auth:
            path = os.getcwdb()
            print(path)
            con.send(path)
        elif n_msg[0] == 'CHDIR' and auth:
            try:
                os.chdir(n_msg[1])
                con.send(b'SUCCESS')
            except :
                con.send(b'ERROR')
        elif n_msg[0] == 'GETFILES' and auth:
            files = []
            with os.scandir() as it:
                for entry in it:
                    if entry.is_file():
                        files.append(entry.name)
            n_files = str(len(files)).encode('utf-8')
            res = '\n'.join(files).encode('utf-8')
            con.send(n_files+b'\n'+res)
        elif n_msg[0] == 'GETDIRS' and auth:
            files = []
            with os.scandir() as it:
                for entry in it:
                    if entry.is_dir():
                        files.append(entry.name)
            n_files = str(len(files)).encode('utf-8')
            res = '\n'.join(files).encode('utf-8')
            con.send(n_files+b'\n'+res)
        elif n_msg[0] == 'EXIT': break
        else:
            con.send(b'ERROR')
        print(cliente, msg)

    print('Finalizando conexao do cliente', cliente)
    con.close()
    _thread.exit()

if __name__ == '__main__':
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    orig = (HOST, PORT)

    tcp.bind(orig)
    tcp.listen(1)

    folder = "/".join(sys.argv[0].split('/')[:-1])
    os.chdir(folder)
    while True:
        con, cliente = tcp.accept()
        _thread.start_new_thread(conectado, tuple([con, cliente]))

    tcp.close()
