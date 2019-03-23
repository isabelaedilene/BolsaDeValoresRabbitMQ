# Bolsa de Valores  
Neste trabalho deverá ser desenvolvido um sistema para uma bolsa de valores qualquer, como a Bovespa, utilizando o RabbitMQ.  
O trabalho consiste em desenvolver um pequeno aplicativo para o Broker e outro aplicativo para a Bolsa de valores, utilizando filas de mensagens. Os requisitos do trabalho são:
1. O endereço do RabbitMQ server deve ser passado como parâmetro para que brokers e bolsas possam escolhem a quem se conectar.
2. A bolsa deve abrir um canal do tipo pub/sub utilizando tópicos para publicar as atualizações no livro de ofertas e as operações realizadas em uma ação. O nome do canal deve ser BOLSADEVALORES.
3. O servidor abre uma fila de mensagens para receber as operações dos clientes. O nome da fila de mensagens deve ser BROKER.
4. Os clientes enviam operações para o servidor através da fila de mensagens BROKER.
5. Todos os clientes devem receber a notificação das operações através da fila BOLSA.
6. O servidor deverá ser disponibilizado em uma máquina diferente de localhost.
7. O aplicativo deve funcionar nas máquinas Linux do laboratório de redes do curso de Engenharia de Software da PUC Minas.


As regras para troca de mensagens são:  
 • Brokers podem enviar ORDENS DE COMPRA, ORDENS DE VENDA e INFO para a bolsa de valores.   
 • Brokers podem assinar tópicos relativos às ações que desejam acompanhar.   
 • Sempre que a bolsa de valores recebe ordem de compra ou de venda, ela deve encaminhar essa ordem a todos os brokers interessados naquela ação específica.   
 • Sempre que o valor de uma ORDEM DE COMPRA for maior ou igual ao valor de uma ORDEM DE VENDA para uma mesma ação, a bolsa de valores deve gerar uma mensagem chamada transacao <quant: int, val: real>, e atualizar/remover as ordens da fila.   
 • A bolsa de valores e os brokers deverão publicar as mensagens usando uma estrutura de tópicos, do tipo: operacao.acao.  
 
 O diagrama de sequência abaixo exibe um cenário de interação na bolsa de valores entre duas corretoras.  
 ![Diagrama de Sequencia](https://imgur.com/3hbO2Q4)  
 

