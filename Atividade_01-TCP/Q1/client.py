# Aluno: Enzo Dornelles Italiano - RA: 2044595
# Aluno: Lucas Henrique Malaquias da Silva Donadi - RA: 1711598
# Descrição: código do servidor para comunicação TCP para questão 1.
# Data de criação: 15/10/2021.
# Atualizações: 16/10/2021, 18/10/2021, 22/10/2021, 24/10/2021.

import socket
import hashlib

# Configurações
HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

COMMANDS = {
    'conn':'CONNECT',
    'pwd':'PWD',
    'cd':'CHDIR',
    'ls':'GETFILES',
    'dir':'GETDIRS',
    'exit':'EXIT'
}

def msgProcessing(msg):
    aux = msg.split()
    if aux[0] == 'conn':
        aux = msg.split(',')
        hash = hashlib.sha512( aux[1].strip().encode("utf-8") ).hexdigest()
        aux = aux[0].split()
        res = f"{COMMANDS[aux[0]]} {aux[1]}, {hash}"
    else:
        try:
            res = f'{COMMANDS[aux[0]]} {" ".join(aux[1:])}'
        except:
            res = f'{aux[0]}'
    return res.encode('utf-8')


if __name__ == '__main__':
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)

    # Comunicação
    msg = input("Cliente:")
    auth = False
    while True:
        # Mensagem enviada
        p_msg = msgProcessing(msg)
        tcp.send(p_msg)

        # Mensagem recebida
        if msg == 'exit': break
        if (msg.split()[0] == 'ls' or msg.split()[0] == 'dir') and auth:
            ans = tcp.recv(1024)
            ans = ans.decode('utf-8')
            print("Servidor: ", ans)
        else:
            ans = tcp.recv(1024)
            ans = ans.decode('utf-8')
            print("Servidor: ", ans)
            if ans == 'Autenticado': auth = True


        # Próxima mensagem
        msg = input("Cliente:")

    tcp.close()