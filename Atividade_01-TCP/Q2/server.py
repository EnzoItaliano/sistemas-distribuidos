# Aluno: Enzo Dornelles Italiano - RA: 2044595
# Aluno: Lucas Henrique Malaquias da Silva Donadi - RA: 1711598
# Descrição: código do servidor para comunicação TCP para questão 2.
# Data de criação: 15/10/2021.
# Atualizações: 16/10/2021, 18/10/2021, 22/10/2021, 24/10/2021, 25/10/2021.

import socket
import _thread
import sys
import os

HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

COMMANDS = {
    1:'ADDFILE',
    2:'DELETE',
    3:'GETFILESLIST',
    4:'GETFILE'
}

# Decodifica bloco recebido
def msgRecvProcessing(msg):
    msg_type = int.from_bytes(msg[:1], byteorder='big')
    msg_id = int.from_bytes(msg[1:2], byteorder='big')
    msg_filename_size = int.from_bytes(msg[2:3], byteorder='big')
    msg_filename = msg[3:255].decode('utf-8')
    print('msg info:', msg_type, msg_id, msg_filename_size, msg_filename)
    return msg_type, msg_id, msg_filename_size, msg_filename

# Cria bloco padrão de envio
def msgSendProcessing(msg_id, res_status):
    msg_send = b'\x02'
    msg_send += (msg_id).to_bytes(1, byteorder='big')
    msg_send += (res_status).to_bytes(1, byteorder='big')

    return msg_send

def conectado(con, cliente):
    print('Conectado por', cliente)
    while True:
        msg = con.recv(1024)
        if not msg: break

        msg_type, msg_id, msg_filename_size, msg_filename = msgRecvProcessing(msg)
        if msg_type != 1:
            con.send(b'Comando nao reconhecido')
            continue
        if COMMANDS[msg_id] == 'ADDFILE': # Adiciona arquivo ao servidor
            file_info = con.recv(1024)
            file_size = int.from_bytes(file_info[:4], byteorder='big')
            file_msg = file_info[4:].decode('utf-8')

            try:
                with open(msg_filename, 'w+b') as file:
                    for i in range(file_size):
                        byte = file_msg[i].encode('utf-8')
                        file.write(byte)
                msg_send = msgSendProcessing(msg_id,1)
            except:
                msg_send = msgSendProcessing(msg_id,2)

            con.send(msg_send)

        elif COMMANDS[msg_id] == 'GETFILESLIST': # Lista arquivos do diretorio
            try:
                files = []
                with os.scandir() as it:
                    for entry in it:
                        if entry.is_file():
                            files.append((len(entry.name),entry.name))
                n_files = (len(files)).to_bytes(2,byteorder='big')
                res = b''
                for file in files:
                    res += b'\n'
                    res += (file[0]).to_bytes(1, byteorder='big')
                    res += file[1].encode('utf-8')
                msg_send = msgSendProcessing(msg_id,1)
                con.send(msg_send+n_files+res)
            except:
                msg_send = msgSendProcessing(msg_id,2)
                con.send(msg_send)

        elif COMMANDS[msg_id] == 'DELETE': # Apaga algum arquivo do diretorio
            try:
                os.remove(msg_filename)
                msg_send = msgSendProcessing(msg_id,1)
                con.send(msg_send+n_files+res)
            except:
                msg_send = msgSendProcessing(msg_id,2)
                con.send(msg_send)
           
        elif COMMANDS[msg_id] == 'GETFILE': # Baixa arquivo do diretorio
            try:
                with os.scandir() as it:
                    for entry in it:
                        if entry.is_file() and entry.name == msg_filename:
                            file_info = os.stat(msg_filename)
                            file_msg = (file_info.st_size).to_bytes(4, byteorder='big')
                            with open(msg_filename, 'rb') as file:
                                byte = file.read(1)
                                while byte != b'':
                                    file_msg += byte
                                    byte = file.read(1)
                msg_send = msgSendProcessing(msg_id,1)
                con.send(msg_send+file_msg)
            except:
                msg_send = msgSendProcessing(msg_id,2)
                con.send(msg_send)

        else:
            con.send(b'Recebido')
        
        print(cliente, msg)

    print('Finalizando conexao do cliente', cliente)
    con.close()
    _thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

# Entra na pasta compartilhada do servidor
folder = "/".join(sys.argv[0].split('/')[:-1])
os.chdir(folder)
folder = f'./server_folder'
os.chdir(folder)
while True:
    con, cliente = tcp.accept()
    _thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()