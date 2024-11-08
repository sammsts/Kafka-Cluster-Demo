# Kafka Cluster Demo com Docker e Aplicação Python

Este projeto demonstra a configuração de um cluster Apache Kafka com múltiplos brokers e uma aplicação Python que consome, processa e produz mensagens entre tópicos. Todo o ambiente é configurado usando Docker e Docker Compose.

## Pré-requisitos

Antes de iniciar, verifique se você tem o **Docker** e o **Docker Compose** instalados no seu sistema. 

- [Instalar Docker](https://docs.docker.com/get-docker/)
- [Instalar Docker Compose](https://docs.docker.com/compose/install/)

## Estrutura do Projeto

- `docker-compose.yml`: Configura e define todos os serviços (Zookeeper, brokers Kafka, e aplicação Python).
- `Dockerfile-python`: Arquivo Docker para a aplicação Python.
- `requirements.txt`: Lista de dependências da aplicação Python.
- `streaming.py`: Script Python que consome, processa e produz mensagens no Kafka.

## Instruções de Instalação e Execução

1. **Clone o Repositório**
   Clone este repositório para o seu ambiente local:

   ```bash
   git clone https://github.com/seuusuario/kafka-cluster-demo.git
   cd kafka-cluster-demo

2. **Inicie o Ambiente com Docker Compose**
   Use o Docker Compose para construir e iniciar todos os serviços em segundo plano:
   
   ```bash
   docker-compose up -d --build
   ```
   
  Esse comando:
  <ul>
    <li>Constrói a imagem da aplicação Python (python-app) usando o Dockerfile-python.</li>
    <li>Inicia o Zookeeper, três brokers Kafka (kafka1, kafka2, kafka3), e a aplicação Python.</li>
    <li>Cria automaticamente os tópicos meu_topico e topicos_processados através do serviço topic-creator.</li>
  </ul>

3. **Verifique se os Serviços Estão Ativos**
   Para confirmar que todos os serviços estão em execução, utilize:

  ```bash
  docker-compose ps
  ```

  Todos os containers devem estar no status "Up".

## Testando o Funcionamento
   Para verificar se o fluxo de dados está funcionando corretamente entre os tópicos meu_topico e topicos_processados, siga os passos abaixo:

   1. **Publicar Mensagens no Tópico Principal (meu_topico)**
      Use o kafka-console-producer para enviar mensagens para o tópico meu_topico:

      ```bash
      docker exec -it kafka1 kafka-console-producer --topic meu_topico --bootstrap-server kafka1:9092
      ```
      
      Digite uma mensagem e pressione Enter. Cada linha que você enviar será processada pelo python-app.

  2. **Verificar Mensagens Processadas no Tópico topicos_processados**
     Use o kafka-console-consumer para ler as mensagens processadas e publicadas no tópico topicos_processados:

     ```bash
      docker exec -it kafka1 kafka-console-consumer --topic topicos_processados --bootstrap-server kafka1:9092 --from-beginning
      ```

     Você deve ver a saída do processamento, onde cada mensagem contém o texto original e uma contagem de palavras.

## Estrutura do Código (Explicação do streaming.py)
  # O arquivo streaming.py realiza as seguintes operações:
  <ul>
    <li>Consome mensagens do tópico meu_topico: Lê mensagens publicadas no tópico principal.</li>
    <li>Processa cada mensagem: Conta o número de palavras na mensagem recebida.</li>
    <li>Produz mensagens para o tópico topicos_processados: Envia o resultado do processamento para um novo tópico.</li>
  </ul>

## Problemas Comuns
  <ul>
    <li>Erro de Conexão com Kafka: Se o python-app não conseguir se conectar aos brokers, verifique se todos os brokers e o Zookeeper estão ativos e rodando.</li>
    <li>Erro Connection refused: Isso pode ocorrer se o python-app iniciar antes dos brokers Kafka. Nesse caso, reinicie o python-app:</li>
  </ul>
  
  ```bash
    docker-compose restart python-app
  ```

## Parar o Ambiente
  Para parar e remover todos os containers, use:
  
  ```bash
    docker-compose down
  ```
