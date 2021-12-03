# Aluno: Enzo Dornelles Italiano - RA: 2044595
# Aluno: Lucas Henrique Malaquias da Silva Donadi - RA: 1711598
# Descrição: Chat P2P para dois usuários permitindo o uso de emoji, URL, texto e uma
# mensagem de teste para verificação se o outro usuário ainda está ativo.
# Data de criação: 29/10/2021.
# Atualizações: 30/10/2021, 31/10/2021, 01/10/2021.

import socket
import random
import re
import emoji
import threading

# Configurações
HOST = '127.0.0.1'      # Endereco IP da comunicação
PORT = 5000             # Porta para comunicação

TIPOS_NUM = {
    1: "normal",
    2: "emoji",
    3: "URL",
    4: "ECHO"
}

TIPOS_STR = {
    "normal":   1,
    "emoji":    2,
    "URL":      3,
    "ECHO":     4
}

# Verifica existência de emoji na mensagem
def text_has_emoji(text):
    text = text.split()
    for word in text:
        if emoji.is_emoji(word):
            return True
    return False

# Trata recebimento de mensagens
def msg_recebida(udp, src, dest):
    while True:
        msg_rec = udp.recvfrom(1024)
        msg_rec = msg_rec[0]

        # Tipo da mensagem
        msg_type = int.from_bytes(msg_rec[:1], byteorder='big')
        # Tamanho nome usuario
        msg_user_len = int.from_bytes(msg_rec[1:2], byteorder='big')
        # Nome usuario
        msg_user = msg_rec[2:(msg_user_len+2)].decode('utf-8')
        # Tamanho da msg
        msg_len = int.from_bytes(msg_rec[(msg_user_len+2):(msg_user_len+3)], byteorder='big')
        # Texto da msg
        msg_txt = msg_rec[(msg_user_len+3):].decode('utf-8')

        if TIPOS_NUM[msg_type] == 'ECHO':
            echo_msg = (TIPOS_STR["normal"]).to_bytes(1, byteorder='big')
            echo_msg += (msg_user_len).to_bytes(1, byteorder='big')
            echo_msg += msg_user.encode('utf-8')
            echo_msg += (msg_len).to_bytes(1, byteorder='big')
            echo_msg += msg_txt.encode('utf-8')[:255]
            udp.sendto(echo_msg, dest)
        elif TIPOS_NUM[msg_type] == 'emoji':
            print(emoji.emojize(msg_txt, use_aliases=True))
        else:
            print(f"\n{msg_user}:{msg_txt}")

if __name__ == '__main__':
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Um cliente escuta onde o outro envia e vice versa
    listen_port = (HOST, PORT)
    send_port = (HOST, PORT+1)
    try:
        udp.bind(listen_port)
    except:
        listen_port = send_port
        send_port = (HOST, PORT)
        udp.bind(listen_port)

    # Escolha de nome de usuario
    user = input('Usuario: ')[:64]
    if user == '':
        user = 'Usuario {}'.format((random.randint(1,100)))
    tam_user = len(user)

    # Thread de recebimento de mensagens
    x = threading.Thread(target=msg_recebida, args=(udp, listen_port, send_port))
    x.start()
    
    # Comunicação
    msg = input(f"{user}:")
    while True:
        if re.search("(https:\/\/)|(http:\/\/)", msg):
            envio_msg = (TIPOS_STR["URL"]).to_bytes(1, byteorder='big')
        elif msg[:4] == 'ECHO':
            envio_msg = (TIPOS_STR["ECHO"]).to_bytes(1, byteorder='big')
        elif text_has_emoji(emoji.emojize(msg, use_aliases=True)):
            envio_msg = (TIPOS_STR["emoji"]).to_bytes(1, byteorder='big')
        else:
            envio_msg = (TIPOS_STR["normal"]).to_bytes(1, byteorder='big')

        envio_msg += tam_user.to_bytes(1, byteorder='big')
        envio_msg += user.encode('utf-8')
        envio_msg += len(msg).to_bytes(1, byteorder='big')
        envio_msg += msg.encode('utf-8')[:255]

        udp.sendto(envio_msg, send_port)

        # Próxima mensagem
        msg = input(f"{user}:")
    x.join()
