import time
import pika

from livro_oferta import Livro

print("Digite o ip para se conectar, se for testar localmente digite localhost")
ip = input()
connection = pika.BlockingConnection(pika.ConnectionParameters(host=ip))
channel = connection.channel()

livro_ofertas = Livro()

#  Declaração de Filas
channel.queue_declare(queue='BROKER_TASK', durable=True)  # Fila que vai enviar operações para a bolsa
channel.queue_declare(queue='BOLSA', durable=True)  # Fila que vai receber operações da bolsa

# Criação da exchange
channel.exchange_declare(exchange='BOLSADEVALORES', exchange_type='topic')
print(' [*] Esperando mensagens. Para sair pressione CTRL+C')


# Processar mensagens, regras de negócio de venda de ações no método do livro de ofertas
def send_messages(msg):
    msg_convertida = "".join(map(chr, msg))
    topic = "*." + msg_convertida.split('.', 1)[1].split('<', 1)[0] + ".*"  # msg em formato bytes, convert para string
    channel.basic_publish(exchange='BOLSADEVALORES', routing_key=topic, body=msg)
    msg_processadas = livro_ofertas.enviar_mensagens_para_fila(msg_convertida)
    for msgs in msg_processadas:
        msg_bytes = bytes(msgs, 'utf-8')
        channel.basic_publish(exchange='BOLSADEVALORES', routing_key=topic, body=msg_bytes)
        print(" Enviando mensagens aos brokers interessados %r : %r" % (topic, msgs))


def callback(ch, method, properties, body):
    msg_convertida = "".join(map(chr, body))
    print(" [x] Mensagem Recebida do broker%r" % msg_convertida)
    print(" [x] Processando")
    time.sleep(2)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    send_messages(body)  # Após processamento a mensagem será enviada de volta ao publish/broker por esse método


channel.basic_consume(on_message_callback=callback, queue='BROKER_TASK')
channel.start_consuming()
