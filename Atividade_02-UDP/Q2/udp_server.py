# Aluno: Enzo Dornelles Italiano - RA: 2044595
# Aluno: Lucas Henrique Malaquias da Silva Donadi - RA: 1711598
# Descrição: Servidor que recebe arquivos vindos de um cliente e os armazena em uma pasta padrão
# Data de criação: 31/10/2021.
# Atualizações: 01/10/2021.

import socket
import hashlib

UDP_IP = "127.0.0.1"                # Endereço IP do servidor
UDP_PORT = 5005                     # Porta do servidor

udp = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
udp.bind((UDP_IP, UDP_PORT))

# Funcao que trata as mensagens recebidas
def rcv_msg(udp, dest):
    file_size = 0           # Tamanho total do arquivo
    filename = ""           # Nome do arquivo
    key = hashlib.sha1()    # Cria uma chave hash
    while True:
        data, addr = udp.recvfrom(1024)
        if int.from_bytes(data[:1], byteorder='big') == 0:
            file_size = int.from_bytes(data[1:5], byteorder='big')
            filename_size = int.from_bytes(data[5:6], byteorder='big')
            filename = data[6:(filename_size+6)].decode('utf-8')
            key = hashlib.sha1()                                        # Reseta a chave hash a cada arquivo novo
        elif int.from_bytes(data[:1], byteorder='big') == 1:            # Trata o primeiro pacote de 1024 bytes
            data = data[1:].decode('ISO8859-1')                         # Utiliza enconding de PDF
            with open(f"./server/{filename}", 'wb') as file:
                byte = data.encode('ISO8859-1')
                key.update(byte)
                file.write(byte)
        elif int.from_bytes(data[:1], byteorder='big') == 2:            # Os pacotes seguintes ao primeiro fazem append no arquivo
            data = data[1:].decode('ISO8859-1')
            with open(f"./server/{filename}", 'ab') as file:
                byte = data.encode('ISO8859-1')
                key.update(byte)
                file.write(byte)
                    
        else:                                                           # Compara as hashes
            if key.hexdigest() == data[1:].decode('utf-8'):
                print("SUCCESS")
            else:
                print("ERROR")

rcv_msg(udp, (UDP_IP, UDP_PORT))