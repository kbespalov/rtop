import pickle
import pika
import config
import metrics.meter as meter
import socket


class PostMan(object):
    EXCHANGE = "rtop"
    TYPE = 'fanout'

    def __init__(self, instance_name, host, port=5672, login="guest", password="guest", emit_delay=20):
        self.instance_name = instance_name
        self.host = host
        self.port = port
        self.username = login
        self.password = password
        self.connection = None
        self.channel = None
        self.isActive = True
        self.emit_delay = emit_delay
        self.stat_producer = meter.metric_producer(self.emit_delay)

    def _connection_params(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        return pika.ConnectionParameters(host=self.host,
                                         port=self.port,
                                         credentials=credentials)

    def _connect(self):
        self.connection = pika.BlockingConnection(self._connection_params())
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.EXCHANGE, type=self.TYPE)

    def emit_loop(self):
        self._connect()
        for stat in self.stat_producer:
            stat['instance'] = self.instance_name
            print stat
            self.channel.basic_publish(exchange=self.EXCHANGE, body=pickle.dumps(stat), routing_key='',
                                       properties=pika.BasicProperties(content_type="text/plain"))


postman = PostMan(socket.gethostname(), config.mq_host, login=config.mq_username, password=config.mq_password)
postman.emit_loop()
