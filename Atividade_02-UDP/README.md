
# Atividade UDP

Alunos:  
Enzo Dornelles Italiano - RA 2044595  
Lucas Henrique Malaquias da Silva Donadi - RA: 1711598

## Bibliotecas
A única biblioteca que não é nativa do pacote Python é a `emoji`.  
A biblioteca emoji fornece códigos de emoji definidos pelo padrão unicode.

## Como executar
Questão 1:
- Em um terminal, executar dentro do diretório "Q1", o comando ```python3 udp_client_p2p.py```
- Em outro terminal, executar dentro do diretório "Q1", o comando ```python3 udp_client_p2p.py```

Questão 2:
- Em um terminal rodar, dentro do diretório "Q2", o comando ```python3 udp_server.py```
- Em outro terminal rodar, dentro do diretório "Q2", o comando ```python3 udp_client.py```

## Exemplos
Questão 1 - Depois de executar os dois passos citados acima você pode começar a envia mensagens
de texto, emojis, URLs e o código ECHO para saber se o outro terminal ainda está ativo.  
Para enviar emojis estamos utilizando a biblioteca emoji do python portanto deve se seguir o nome
usado por ela, como por exemplo :thumbs_up:. Códigos unicode não funcionam porém você pode usar
o nome no padrão CLDR Short Name substituindo espaços por `_`.  
Para que o terminal reconheça URLs, a mensagem deve conter `http`ou `https`.  
Para utilizar o ECHO basta digitar por exemplo `ECHO teste`.

Questão 2 - Depois de executar os dois passos citados acima, na janela do cliente você pode enviar
arquivos utilizando o comando `send <nome_do_arquivo>`. Envie apenas um arquivo por vez. Ao final
do envio após a verificação da integridade do arquivo, o terminal responderá como `SUCCESS` caso
caso tenha dado certo.