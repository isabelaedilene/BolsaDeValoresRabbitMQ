class Livro:

    def __init__(self):
        self.fila_mensagens = []
        self.fila_mensagens_info = []

    def enviar_mensagens_para_fila(self, msg):
        exchange_box = []
        type_of_operation = msg.split('.', 1)[0]  # tipo de operação que vai ser feita, compra ou venda
        if type_of_operation == "info":
            exchange_box = self.verificar_info(msg)
        else:
            self.fila_mensagens.append(msg)
            self.fila_mensagens_info.append(msg)
            exchange_box = self.verificar_compra_venda(msg)
        return exchange_box

    def verificar_info(self, msg):
        acao = msg.split('.', 1)[1].split('<', 1)[0]
        msg_exchange_box = []
        for mensg in self.fila_mensagens_info:
            acao_de_interesse = mensg.split('.', 1)[1].split('<', 1)[0]
            if acao_de_interesse == acao:
                msg_exchange_box.append(mensg)
        return msg_exchange_box

    def verificar_compra_venda(self, msg):
        type_of_operation = msg.split('.', 1)[0]  # tipo de operação que vai ser feita, compra ou venda
        acao = msg.split('.', 1)[1].split('<', 1)[0]  # acao que vai ser verificada
        valor = float(msg.split(';', 1)[1].split(';', 1)[0])  # valor que está comprando ou vendendo FLOAT
        qtd_acoes = int(msg.split('<', 1)[1].split(';', 1)[0])  # quantidade de ações de compra ou de venda INT
        nome = msg.split(';', 1)[1].split('>', 1)[0].split(';', 1)[1]  # nome de quem tá realizando operacao
        msg_exchange_box = []
        if type_of_operation == "compra":
            fila_msg_venda = []  # fila que vai armazenar as mensagens de venda
            for mensagem in self.fila_mensagens:
                msg_venda = mensagem.split('.', 1)[0]
                acao_de_interesse = mensagem.split('.', 1)[1].split('<', 1)[0]
                if msg_venda == "venda" and acao_de_interesse == acao:
                    fila_msg_venda.append(mensagem)
            if fila_msg_venda:
                fila_msg_venda_ordenada = sorted(fila_msg_venda, key=lambda x: float(x.split(';')[1].strip()))
                valor_de_venda = float(fila_msg_venda_ordenada[0].split(';', 1)[1].split(';', 1)[0])
                qtd_acoes_venda = int(fila_msg_venda_ordenada[0].split('<', 1)[1].split(';', 1)[0])
                nome_vendedor = fila_msg_venda_ordenada[0].split(';', 1)[1].split('>', 1)[0].split(';', 1)[1]
                if valor >= valor_de_venda:
                    msg_para_propagar = ""  # mensagem que será enviada a exchange BOLSADEVALORES
                    msg_propagar_continua_operacao = ""  # caso nem todas as ações sejam comprada, é necessário manter a mensagem
                    if qtd_acoes - qtd_acoes_venda == 0:
                        msg_para_propagar = "transacao." + acao + "<" + str(qtd_acoes) + ";" + str(valor) + ">"
                        msg_para_remover = fila_msg_venda_ordenada[0]
                        self.fila_mensagens.remove(msg_para_remover)  # remove msg de venda da fila
                        self.fila_mensagens.remove(msg)  # remove msg de compra
                        self.fila_mensagens_info.append(msg_para_propagar)
                        msg_exchange_box.append(msg_para_propagar)
                    elif qtd_acoes - qtd_acoes_venda > 0:
                        msg_para_propagar = "transacao." + acao + "<" + str(qtd_acoes) + ";" + str(valor) + ">"
                        msg_propagar_continua_operacao = "compra." + acao + "<" + str(qtd_acoes-qtd_acoes_venda) + ";" + str(valor) + nome
                        msg_para_remover = fila_msg_venda_ordenada[0]
                        self.fila_mensagens.remove(msg_para_remover)  # remove msg de venda da fila
                        self.fila_mensagens_info.append(msg_para_propagar)
                        self.fila_mensagens_info.append(msg_propagar_continua_operacao)  # adiciona mensagem atualizada na fila
                        self.fila_mensagens.append(msg_propagar_continua_operacao)
                        msg_exchange_box.append(msg_para_propagar)
                        msg_exchange_box.append(msg_propagar_continua_operacao)
                    else:
                        msg_para_propagar = "transacao." + acao + "<" + str(qtd_acoes) + ";" + str(valor) + ">"
                        msg_propagar_continua_operacao = "venda." + acao + "<" + str(qtd_acoes_venda-qtd_acoes) + ";" + str(valor_de_venda) + ";" + nome_vendedor
                        msg_para_remover = fila_msg_venda_ordenada[0]
                        self.fila_mensagens.remove(msg)
                        self.fila_mensagens.remove(msg_para_remover)
                        self.fila_mensagens_info.append(msg_para_propagar)
                        self.fila_mensagens_info.append(msg_propagar_continua_operacao)
                        self.fila_mensagens.append(msg_propagar_continua_operacao)
                        msg_exchange_box.append(msg_para_propagar)
                        msg_exchange_box.append(msg_propagar_continua_operacao)
        return msg_exchange_box
