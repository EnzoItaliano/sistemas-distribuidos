# Aluno: Enzo Dornelles Italiano - RA: 2044595
# Aluno: Lucas Henrique Malaquias da Silva Donadi - RA: 1711598
# Descrição: Coletor que faz extrai os tweets do dataset e os envia para a fila de mensagens em formato JSON.
# Data de criação: 07/12/2021.
# Atualizações: 07/12/2021, 08/12/2021 e 09/12/2021.

import pika, sys, json, pandas as pd


if __name__ == '__main__':
    # conexao com a lista de mensagens (RabbitMQ)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    #declaracao da queue de mensagens
    channel.queue_declare(queue='tweetsList')

    # declara "data" para receber o dataset a ser utilizado
    data = pd.read_csv('../data/premier league teams 2020-09-20 till 2020-10-13.csv').to_dict('records')

    # publica as mensagens de acordo com a routing key = "tweetList" no formato JSON
    for line in data:
        channel.basic_publish(exchange='', routing_key='tweetsList', body=json.dumps(line))

    # fecha a conexãos
    connection.close()