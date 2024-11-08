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

# Documentação do Projeto Kafka Cluster Demo

## 1. Configuração do Cluster

- **Função do Zookeeper e Interação com os Brokers Kafka**:
  O Zookeeper é responsável por gerenciar e coordenar o cluster Kafka. Ele armazena informações de configuração e estado dos brokers Kafka, ajuda a coordenar as réplicas de partições e facilita a eleição de líderes para as partições. Ele atua como um registro centralizado que mantém o estado dos brokers e garante que o Kafka opere de forma coordenada e resiliente.

- **Configurações Ajustadas no Arquivo `server.properties` para Cada Broker**:
  Neste projeto, as configurações dos brokers foram definidas diretamente no `docker-compose.yml`, em vez de um arquivo `server.properties`. As configurações incluem:
    - `KAFKA_BROKER_ID`: ID único para cada broker no cluster.
    - `KAFKA_ZOOKEEPER_CONNECT`: URL do Zookeeper para que os brokers possam se conectar e coordenar o cluster.
    - `KAFKA_ADVERTISED_LISTENERS` e `KAFKA_LISTENERS`: Endereços e portas que cada broker usará para se comunicar internamente e externamente.
  
  Essas configurações são essenciais para que cada broker identifique sua função no cluster e se conecte adequadamente ao Zookeeper e aos outros brokers.

## 2. Criação de Tópico e Particionamento

- **Número de Partições e Fator de Replicação**:
  O projeto utiliza 3 partições e um fator de replicação de 2. Essas escolhas permitem que o Kafka distribua as mensagens entre múltiplos brokers, aumentando a disponibilidade e a tolerância a falhas. Com 3 partições, o Kafka pode processar mensagens em paralelo, melhorando o desempenho. O fator de replicação 2 garante que, mesmo se um broker falhar, as mensagens estarão disponíveis em outro broker, aumentando a confiabilidade.

- **Distribuição de Mensagens pelas Partições e Impacto na Ordem das Mensagens**:
  O Kafka distribui mensagens entre as partições com base em uma chave de partição, se especificada, ou de maneira aleatória. Esse particionamento permite que o Kafka processe mensagens em paralelo, mas também significa que a ordem das mensagens é garantida apenas dentro de uma única partição, não entre partições. Isso pode impactar o processamento de mensagens que dependem de uma ordem estrita.

## 3. Produção e Consumo de Mensagens

- **Passos para Produzir e Consumir Mensagens**:
  Para produzir mensagens, usamos o `kafka-console-producer`, que permite enviar mensagens ao tópico `meu_topico`. Para consumir, utilizamos o `kafka-console-consumer` para visualizar as mensagens no tópico `topicos_processados`. O script `streaming.py` também realiza a produção e o consumo de mensagens automaticamente.

- **Confiabilidade na Entrega de Mensagens e Falha de Broker**:
  O Kafka garante a confiabilidade das mensagens usando o fator de replicação e as configurações de confirmação (`acks`). Quando um broker falha, os outros brokers podem assumir o controle das partições replicadas, garantindo a disponibilidade das mensagens. A aplicação Python também utiliza o Kafka para gerenciar confirmações de leitura de mensagens (`commit`), garantindo que as mensagens não sejam processadas novamente em caso de falha do consumidor.

## 4. Aplicação de Streaming

- **Funcionalidade da Aplicação de Streaming e Tipo de Processamento**:
  A aplicação de streaming (`streaming.py`) lê mensagens do tópico `meu_topico`, processa cada mensagem contando o número de palavras, e publica o resultado no tópico `topicos_processados`.

- **Como a Aplicação Lê de um Tópico e Grava em Outro e Verificação do Processamento**:
  A aplicação consome mensagens de `meu_topico` usando o `Consumer` da biblioteca `confluent_kafka`. Depois de processar cada mensagem, o resultado é enviado para `topicos_processados` usando o `Producer`. Verificamos o sucesso do processamento visualizando o tópico `topicos_processados` com o `kafka-console-consumer` para ver as mensagens processadas.

## 5. Desafios e Solução de Problemas

- **Problemas com Comunicação entre Brokers, Zookeeper, e Produtor/Consumidor**:
  Problemas comuns incluem falhas de conexão entre o `python-app` e os brokers Kafka, geralmente causadas pela ordem de inicialização dos containers ou breves tempos de inatividade. Outro desafio comum foi garantir que os tópicos fossem criados antes de o `python-app` iniciar.

- **Ferramentas ou Métodos para Monitorar o Cluster e Resolver Problemas**:
  Utilizamos o comando `docker logs` para monitorar os logs dos brokers Kafka, do Zookeeper e do `python-app`, o que ajudou a identificar erros de conexão e falhas de configuração. Além disso, verificamos a conectividade de rede entre os containers usando o comando `nc` para diagnosticar problemas de conexão entre os serviços.

---

O projeto está bem estruturado para permitir uma boa observabilidade e resolução de problemas básicos, além de demonstrar as práticas de configuração e uso do Kafka com um cluster Dockerizado.
