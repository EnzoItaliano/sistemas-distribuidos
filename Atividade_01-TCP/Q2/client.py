# Aluno: Enzo Dornelles Italiano - RA: 2044595
# Aluno: Lucas Henrique Malaquias da Silva Donadi - RA-1711598
# Descrição: código do cliente para comunicação TCP para a questão 2.
# Data de criação: 15/10/2021.
# Atualizações: 16/10/2021, 18/10/2021, 22/10/2021, 24/10/2021, 25/10/2021.

import socket
import os

# Configurações
HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

COMMANDS = {
    'ADDFILE':      1,
    'DELETE':       2,
    'GETFILESLIST': 3,
    'GETFILE':      4
}

def msgProcessing(msg):
    msg = msg.split()
    if msg[0] in COMMANDS and COMMANDS[msg[0]] != 3:
        msg_send = b'\x01'
        msg_send += (COMMANDS[msg[0]]).to_bytes(1, byteorder='big')
        msg_send += (len(msg[1])).to_bytes(1, byteorder='big')
        msg_send += f'{msg[1]}'.encode('utf-8')[:255]
    elif msg[0] in COMMANDS and COMMANDS[msg[0]] == 3:
        msg_send = b'\x01'
        msg_send += (COMMANDS[msg[0]]).to_bytes(1, byteorder='big')
    else:
        msg_send = b'\x00'

    return msg_send
    

if __name__ == '__main__':

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)

    # Comunicação
    msg = input("Cliente:")
    while True:
        # Mensagem enviada
        p_msg = msgProcessing(msg)
        tcp.send(p_msg)

        # Enviando arquivos
        if msg.split()[0] == 'ADDFILE':
            file_info = os.stat(msg.split()[1])
            file_msg = (file_info.st_size).to_bytes(4, byteorder='big')

            with open(msg.split()[1], 'rb') as file:
                byte = file.read(1)
                while byte != b'':
                    file_msg += byte
                    byte = file.read(1)
            tcp.send(file_msg)

        # Mensagem recebida
        if msg.split()[0] == 'ADDFILE':
            ans = tcp.recv(1024)
            res = int.from_bytes(ans[:1], byteorder='big')
            res_type = int.from_bytes(ans[1:2], byteorder='big')
            res_status = int.from_bytes(ans[2:3], byteorder='big')
            for command in COMMANDS:
                if COMMANDS[command] == res_type:
                    if res_status == 1:
                        print(f"Servidor: RESPOSTA {command} SUCCESS")
                    else:
                        print(f"Servidor: RESPOSTA {command} ERROR")

        elif msg.split()[0] == 'GETFILESLIST':
            ans = tcp.recv(1024)
            res = int.from_bytes(ans[:1], byteorder='big')
            res_type = int.from_bytes(ans[1:2], byteorder='big')
            res_status = int.from_bytes(ans[2:3], byteorder='big')
            for command in COMMANDS:
                if COMMANDS[command] == res_type:
                    if res_status == 1:
                        print(f"Servidor: RESPOSTA {command} SUCCESS")
                        files_number = int.from_bytes(ans[3:5], byteorder='big')
                        print("Servidor: ", files_number)
                        files = ans.split(b'\n')
                        for file in files[1:]:
                            print(f"{int.from_bytes(file[:1], byteorder='big')} {file[1:].decode('utf-8')}")
                    else:
                        print(f"Servidor: RESPOSTA {command} ERROR")

        elif msg.split()[0] == 'DELETE':
            ans = tcp.recv(1024)
            res = int.from_bytes(ans[:1], byteorder='big')
            res_type = int.from_bytes(ans[1:2], byteorder='big')
            res_status = int.from_bytes(ans[2:3], byteorder='big')
            for command in COMMANDS:
                if COMMANDS[command] == res_type:
                    if res_status == 1:
                        print(f"Servidor: RESPOSTA {command} SUCCESS")
                    else:
                        print(f"Servidor: RESPOSTA {command} ERROR")

        elif msg.split()[0] == 'GETFILE':
            ans = tcp.recv(1024)
            res = int.from_bytes(ans[:1], byteorder='big')
            res_type = int.from_bytes(ans[1:2], byteorder='big')
            res_status = int.from_bytes(ans[2:3], byteorder='big')
            for command in COMMANDS:
                if COMMANDS[command] == res_type:
                    if res_status == 1:
                        print(f"Servidor: RESPOSTA {command} SUCCESS")
                        file_size = int.from_bytes(ans[3:7], byteorder='big')
                        file_msg = ans[7:].decode('utf-8')
                        with open(msg.split()[1], 'w+b') as file:
                            for i in range(file_size):
                                byte = file_msg[i].encode('utf-8')
                                file.write(byte)
                    else:
                        print(f"Servidor: RESPOSTA {command} ERROR")
            
        # Próxima mensagem
        msg = input("Cliente:")
        if msg == 'EXIT' or msg == 'exit': break

    tcp.close()