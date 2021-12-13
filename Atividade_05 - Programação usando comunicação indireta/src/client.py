# Aluno: Enzo Dornelles Italiano - RA: 2044595
# Aluno: Lucas Henrique Malaquias da Silva Donadi - RA: 1711598
# Descrição: Cliente que faz a seleção do tópico de assinatura e imprimi os tweets depois.
# Data de criação: 07/12/2021.
# Atualizações: 07/12/2021, 08/12/2021 e 09/12/2021.

import pika, sys, os, json


def main():
    # seleção do tópico a ser entregue ao assinante
    request_type = int(input('\nSelecione um time para receber os tweets - Manchester United (1), Liverpool (2) ou Chelsea (3): '))
    while request_type > 3 or request_type < 1:
            print("Não conheço esse tópico.\n")
            request_type = int(input('\nSelecione um time para receber os tweets - Manchester United (1), Liverpool (2) ou Chelsea (3): '))

    if request_type == 1:
        name_queue = 'ManchesterUnited'
    elif request_type == 2:
        name_queue = 'Liverpool'
    elif request_type == 3:
        name_queue = 'Chelsea'
    filename = name_queue + '.log'

    # conexao com a lista de mensagens (RabbitMQ)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # cria o canal de mensagens, caso nao esteja criado ainda
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    # declaracao da queue de mensagens
    result = channel.queue_declare(queue='', exclusive=False)
    queue_name = result.method.queue

    # vincula a queue a exchange especifica
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=name_queue)

    print(' [*] Aguardando os tweets. CTRL+C para finalizar')

    # função para imprimir os tweets de interesse do assinante
    def callback(ch, method, properties, body):
        data = json.loads(body)
        message = f'------------------\n' \
            + f'\tTópico sobre: {data["file_name"]}\n' \
            + f'\tUsuário: {data["username"]}\n' \
            + f'\tTweet ID: {data["twitter_id"]}\n' \
            + f'\tTweet: {data["text"]}\n' \
            + f'\tCriado em: {data["created_at"]}\n' \
            + f'\tRetweets: {data["retweet_count"]}\n' \
            + '------------------\n'

        print(message) 

    # consome mensagens de binds 
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # inicia o consumo de mensagens
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrompido')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)