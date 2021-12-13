
# Atividade UDP

Alunos:  
Enzo Dornelles Italiano - RA 2044595  
Lucas Henrique Malaquias da Silva Donadi - RA: 1711598

## Bibliotecas
As bibliotecas que foram utilizadas:
- Pika, Pandas e Json

## Como executar
- Em um terminal, executar o cliente dentro do diretório /src/ --> python client.py
- Em outro terminal, executar o classificador dentro do diretório /src/ --> python classifier.py
- E por fim, no terceiro terminal, executar o coletor dentro do diretório /src/ --> python collector.py

## Exemplo
Você executa o cliente, escolhe o tópico relacionado ao Manchester United. Após isso executa o classificador que fica esperando o coletor enviar as mensagens para a fila. Com a execução do coletor, o classificador acessa a fila e determina quais tweets são do tópico desejado pelo assinante, após isso os tweets selecionados voltam pra fila e são consumidos pelo cliente que os imprime.