from typing import List
from kombu import Connection, Exchange, Producer, Queue
from kombu.mixins import ConsumerMixin


# The basic class ConsumerMixin would need a :attr:`connection` attribute
# which must be a :class:`~kombu.Connection` instance,
# and define a :meth:`get_consumers` method that returns a list of :class:`kombu.Consumer` instances to use.
class Worker(ConsumerMixin):
  def __init__(
      self,
      connection: Connection,
      queue_list: List[Queue],
      accept_type: List[str],
  ):
    self.connection = connection
    self.queue_list = queue_list
    self.accept_type = accept_type

  def get_consumers(self, Consumer, channel):
    return [Consumer(
        queues=self.queue_list,
        accept=self.accept_type,
        callbacks=[self.on_task]
    )]

  def on_task(self, body, message):
    try:
        print(body)
    except Exception as exc:
        print("task raised exception: %r", exc)
    message.ack()


class ClueMQ:
  def __init__(
      self,
      host: str = "localhost",
      exchange_name: str = "cluemq",
      queue_name: str = "cluemq",
      queue_routing_key: str = "cluemq.test",
      exchange_type: str = "topic",
      accept_type: List[str] = ["json"]
  ):
    self.conn = Connection(host)
    self.exchange_name = exchange_name
    self.exchange_type = exchange_type
    self.exchange = Exchange(
        name=self.exchange_name,
        type=exchange_type,
        channel=self.conn,
        durable=True
    )
    self.queue_name = queue_name
    self.routing_key = queue_routing_key
    self.queue = Queue(
        name=self.queue_name,
        channel=self.conn,
        durable=True,
        auto_delete=False,
        exchange=self.exchange,
        routing_key=self.routing_key
    )
    self.worker = Worker(self.conn, [self.queue], accept_type)

  def connect(self):
    self.conn.connect()
    print("-----Mesage Queue connection connected-----")

  def close(self):
    self.conn.close()
    print("-----Mesage Queue connection closed-----")

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

  def send_message(
      self,
      data: dict,
  ):
    producer = Producer(self.conn)
    producer.publish(
        data,
        exchange=self.exchange,
        routing_key=self.routing_key,
        serializer="json"
    )

  def run(self):
    self.connect()

    try:
        self.worker.run()
    except KeyboardInterrupt:
        print("Terminate worker")

    self.close()
