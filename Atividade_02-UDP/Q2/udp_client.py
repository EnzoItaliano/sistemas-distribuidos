# Aluno: Enzo Dornelles Italiano - RA: 2044595
# Aluno: Lucas Henrique Malaquias da Silva Donadi - RA: 1711598
# Descrição: Cliente para envio de arquivos ao servidor UDP.
# Data de criação: 31/10/2021.
# Atualizações: 01/10/2021.

import socket
import os
import hashlib

UDP_IP = "127.0.0.1"        # Endereço IP do cliente
UDP_PORT = 5005             # Porta do cliente

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

udp = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

if __name__ == '__main__':
    while True:
        message = input()
        msg = message.split()
        # É necessário usar o comando send para enviar arquivos
        if msg[0] == 'send':
            msg_send = (0).to_bytes(1, byteorder='big')                     # ID de identificação do pacote
            file_info = os.stat(msg[1])
            msg_send += (file_info.st_size).to_bytes(4, byteorder='big')    # Tamanho do arquivo a ser enviado
            filename = os.path.basename(msg[1])
            msg_send += len(filename).to_bytes(1, byteorder='big')          # Tamanho do nome do arquivo
            msg_send += os.path.basename(msg[1]).encode('utf-8')            # Nome do arquivo
            key = hashlib.sha1()

            udp.sendto(msg_send, (UDP_IP, UDP_PORT))
            
            file_msg = (1).to_bytes(1, byteorder='big')                     # ID de identificação do pacote, significando inicio do arquivo enviado
            with open(msg[1], 'rb') as file:
                byte = file.read(1)
                count_size = 0
                while byte != b'':                                          # Envio de bytes do arquivo
                    file_msg += byte
                    key.update(byte)
                    byte = file.read(1)
                    count_size += 1
                    if count_size == 1023 or byte == b'':                   # Envia 1023 bytes + ID de identificação em cada pacote
                        udp.sendto(file_msg, (UDP_IP, UDP_PORT))
                        count_size = 0
                        file_msg = (2).to_bytes(1, byteorder='big')         # ID de identificação do pacote, significando partes do arquivo que não é a primeira
            msg_send = (3).to_bytes(1, byteorder='big')                     # ID de identificação do pacote, significando que é o pacote da hash
            msg_send += key.hexdigest().encode('utf-8')
            udp.sendto(msg_send, (UDP_IP, UDP_PORT))