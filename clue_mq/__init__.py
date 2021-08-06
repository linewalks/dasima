from typing import List, Callable
from kombu import Connection, Exchange, Producer, Queue
from kombu.mixins import ConsumerProducerMixin


# The basic class ConsumerMixin would need a :attr:`connection` attribute
# which must be a :class:`~kombu.Connection` instance,
# and define a :meth:`get_consumers` method that returns a list of :class:`kombu.Consumer` instances to use.
class Worker(ConsumerProducerMixin):
  def __init__(
      self,
      connection: Connection,
      queue_list: List[Queue],
      on_task_list: List[Callable],
      accept_type: List[str],
  ):
    self.connection = connection
    self.queue_list = queue_list
    self.on_task_list = on_task_list
    self.accept_type = accept_type

  def get_consumers(self, Consumer, channel):
    return [
        Consumer(
            queues=[queue],
            accept=self.accept_type,
            callbacks=[on_task]
        )
        for queue, on_task in zip(self.queue_list, self.on_task_list)
    ]


class ClueMQ:
  def __init__(
      self,
      host: str = "localhost",
      exchange_name: str = "cluemq",
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
    self.queue_list = []
    self.on_task_list = []
    self.worker = Worker(self.conn, self.queue_list, self.on_task_list, accept_type)

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

  def send_message(
      self,
      data: dict,
      routing_key: str,
      serializer: str = "json"
  ):
    producer = Producer(self.conn)
    producer.publish(
        data,
        exchange=self.exchange,
        routing_key=routing_key,
        serializer=serializer
    )

  def run(self):
    self.connect()

    try:
        self.worker.run()
    except KeyboardInterrupt:
        print("Terminate worker")

    self.close()

  def add_queue(self, exchange, routing_key, func):
    queue_name = func.__name__
    queue = Queue(
        name=queue_name,
        channel=self.conn,
        durable=False,
        auto_delete=False,
        exchange=self.exchange,
        routing_key=routing_key
    )

    def on_task(body, message):
      try:
        result = func(**body)
        print(result)
      except Exception as exc:
        print("task raised exception: %r", exc)
      message.ack()

    queue.declare()
    self.queue_list.append(queue)
    self.on_task_list.append(on_task)
