import pika

print("Digite o ip para se conectar, se for testar localmente digite localhost")
ip = input()
connection = pika.BlockingConnection(pika.ConnectionParameters(ip))
channel = connection.channel()

#  Declaração de Filas
channel.queue_declare(queue='BROKER_TASK', durable=True)  # Fila que vai enviar operações para a bolsa
channel.queue_declare(queue='BOLSA', durable=True)  # Fila que vai receber operações da bolsa
result = channel.queue_declare('', exclusive=True)  # Fila que vai ser associada ao tópico
queue_name = result.method.queue

# Criação da exchange
channel.exchange_declare(exchange='BOLSADEVALORES', exchange_type='topic')


def tipo_msg():
    tipo = str(input())
    if tipo == "venda" or tipo == "VENDA":
        return 'venda'
    elif tipo == "compra" or tipo == "COMPRA":
        return "compra"
    elif tipo == "info" or tipo == "INFO":
        return "info"
    else:
        return "erro"


ativos_bolsa = ['ABEV3', 'PETR4', 'VALE5', 'ITUB5', 'BBDC4',
                'BBAS3', 'CIEL3', 'PEETR3', 'HYPE3', 'VALE3',
                'BBSE3', 'CTIP3', 'GGBR4', 'FIBR3', 'RADL3']
key_topico = 'topico'


def info_from_user():
    print("Digite seu nome")
    nome = input()
    print("Mensagens podem ser do tipo INFO, COMPRA, VENDA")
    print("Digite o tipo de mensagem que deseja enviar")
    tipo = tipo_msg()
    print("Dos ativos abaixo")
    for ativo in ativos_bolsa:
        print(ativo)
    print("Digite sobre qual ativo deseja operar")
    ativo_escolhido = input()
    global key_topico
    key_topico = get_tipo_msg_topic("*." + ativo_escolhido + ".*")
    if tipo == 'info':
        print("Digite a data que deseja as informações")
        data = input()
        return tipo + "." + ativo_escolhido + "<" + data + ">"
    elif tipo == 'venda':
        print("Digite a quantidade de ações que será vendida")
        qtd_acoes = input()
        print("Digite o valor unitário de cada ação a ser vendida")
        valor_acao = input()
        valor_acao_convertido = float(valor_acao.replace(',', '.'))
        return tipo + "." + ativo_escolhido + "<" + qtd_acoes + ";" + str(valor_acao_convertido) + ";" + nome + ">"
    elif tipo == 'compra':
        print("Digite a quantidade de ações que deseja comprar")
        qtd_compra = input()
        print("Digite o valor unitário de compra de cada ação")
        preco = input()
        preco_convertido = float(preco.replace(',', '.'))
        return tipo + "." + ativo_escolhido + "<" + qtd_compra + ";" + str(preco_convertido) + ";" + nome + ">"
    else:
        print("Tipo de mensagem inválido")


def get_tipo_msg_topic(tipo):
    return tipo


message = info_from_user()  # Nesse momento todas as varáveis vão ser carregadas. (tópicos, routing_key, message, etc)
#  publicando mensagem na fila BROKER
channel.basic_publish(exchange='',
                      routing_key='BROKER_TASK',
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2))
print(" [x] Mensagem enviada à bolsa pelo broker")


# Recebendo mensagens da bolsa, fazendo o binding das filas existentes com os tópicos
channel.queue_bind(exchange='BOLSADEVALORES', queue=queue_name, routing_key=key_topico)
print(' [*] Esperando respostas/mensagens de tópico. Para sair pressione CTRL+C')


def callback(ch, method, properties, body):
    msg_convertida = "".join(map(chr, body))  # mensagem em bytes -> convertendo para string
    print(" [x] %r : %r" % (method.routing_key, msg_convertida))


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
connection.close()
