from kombu import Connection, Exchange, Queue


class ClueMQ:
  def __init__(self, host, exchange, queue, queue_routing_key, exchange_type="topic"):
    self.conn = Connection(host)
    self.exchange_name = exchange
    self.exchange_type = exchange_type
    self.exchange = Exchange(
        name=self.exchange_name,
        type=exchange_type,
        channel=self.conn,
        durable=True
    )
    self.queue_name = queue
    self.routing_key = queue_routing_key
    self.queue = Queue(
      name=self.queue_name,
      channel=self.conn,
      durable=True,
      auto_delete=False,
      exchange=self.exchange,
      routing_key=self.routing_key
   )

  def connect(self):
    self.conn.connect()
    print("-----AMQP connection-----")

  def close(self):
    self.conn.close()
    print("-----AMQP close-----")

  def setup(self):
    self.exchange.declare()
    print("-----declare exchange-----")
    print(f"""
    exchange name: {self.exchange_name},
    exchange type: {self.exchange_type},
    """)
    self.queue.declare()
    print("-----declare queue-----")
    print(f"""
    queue name: {self.queue_name}
    exchange: {self.exchange},
    routing key: {self.routing_key},
    """)
