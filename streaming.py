import os
from confluent_kafka import Consumer, Producer

# Obter o endereço dos brokers a partir das variáveis de ambiente
bootstrap_servers = os.getenv('BOOTSTRAP_SERVERS', 'localhost:9092')

# Configuração do consumidor e produtor
consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'meu_grupo',
    'auto.offset.reset': 'earliest',
    'session.timeout.ms': 6000,  # Aumenta o tempo limite da sessão para evitar desconexões rápidas
    'retries': 5,  # Número de tentativas de reconexão
    'retry.backoff.ms': 500  # Intervalo entre tentativas
})
producer = Producer({
    'bootstrap.servers': bootstrap_servers,
    'retries': 5,  # Número de tentativas de reconexão
    'retry.backoff.ms': 500  # Intervalo entre tentativas
})

# Subscribing to the main topic
consumer.subscribe(['meu_topico'])

# Processa e envia para o tópico de resultados
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Erro: {msg.error()}")
        continue

    text = msg.value().decode('utf-8')
    word_count = len(text.split())
    output = f"Mensagem: {text} | Contagem de Palavras: {word_count}"

    # Envia o resultado para o tópico de processamento
    producer.produce('topicos_processados', output.encode('utf-8'))
    producer.flush()
    print(f"Processado: {output}")

    # Confirmação da mensagem lida
    consumer.commit()
