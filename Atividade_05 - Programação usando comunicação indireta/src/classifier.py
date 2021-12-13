# Aluno: Enzo Dornelles Italiano - RA: 2044595
# Aluno: Lucas Henrique Malaquias da Silva Donadi - RA: 1711598
# Descrição: Classificador que dado o tópico de assinatura, analisa e separa os tweets desejados.
# Data de criação: 07/12/2021.
# Atualizações: 07/12/2021, 08/12/2021 e 09/12/2021.

import pika, sys, os, json, pandas as pd


def main():
    # conexao com a lista de mensagens (RabbitMQ)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    #declaracao da queue de mensagens
    channel.queue_declare(queue='tweetsList')

    # função que classifica os tweets de acordo com o tópico selecionado
    def callback(ch, method, properties, body):
        tweet = json.loads(body)
        tweet_id = tweet['twitter_id']
        tweet_topic = tweet['file_name']

        routing_key = ''

        if tweet_topic == 'ManchesterUnited' :
            routing_key = 'ManchesterUnited'

        elif tweet_topic == 'Liverpool' :
            routing_key = 'Liverpool'

        elif tweet_topic == 'Chelsea' :
            routing_key = 'Chelsea'

        # cria o canal de mensagens, caso nao esteja criado ainda
        channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
        # publica a exchange de mensagens de acordo com a routing key
        channel.basic_publish(exchange='direct_logs', routing_key=routing_key, body=body)
        
        # printa o ID dos tweets classificados como o tópico selecionado
        print(" [x] Classified %r" % tweet_id)

    # consome mensagens de binds 
    channel.basic_consume(queue='tweetsList', on_message_callback=callback, auto_ack=True)

    print(' [*] Esperando por menssagens.')

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