# Atividade Representação Externa de Dados

Alunos:  
Enzo Dornelles Italiano - RA 2044595  
Lucas Henrique Malaquias da Silva Donadi - RA: 1711598

## Bibliotecas
As bibliotecas utilizadas tanto no java quanto no python são padrão para implementação do grpc e SQLite

## Compilar servidor java
`mvn compile`

## Como executar
No servidor em java:
`mvn exec:java -D"exec.mainClass"="Server"`

No cliente em python:
`python3 client.py`

## Exemplos
A aplicação funciona como um gerenciador de matrículas. Na aplicação podemos criar uma matrícula em determinada turma; alterar notas de um aluno; alterar faltas; listar os alunos de uma determinada disciplina, mediante o semestre e o ano; podemos mostrar o boletim de um semestre do aluno; e listar todas as disciplinas de um curso.

