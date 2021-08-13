import threading
from typing import List, Callable
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerProducerMixin

from clue_mq.utils import setup


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
    print("Worker __init__")
    self.connection = connection
    self.queue_list = queue_list
    self.on_task_list = on_task_list
    self.accept_type = accept_type


  def get_consumers(self, Consumer, channel):
    print("Worker get_consumers")
    return [
        Consumer(
            queues=[queue],
            accept=self.accept_type,
            callbacks=[on_task]
        )
        for queue, on_task in zip(self.queue_list, self.on_task_list)
    ]

# ClueMQ clas
class ClueMQ:
  def __init__(
      self,
      host: str = "localhost", # amqp://guest:guest@localhost:5672//
      exchange_name: str = "cluemq",
      exchange_type: str = "topic",
      accept_type: List[str] = ["json"]
  ):
    print("ClueMQ __init__")
    self.conn = Connection(host)
    self.exchange_name = exchange_name
    self.exchange_type = exchange_type
    self.accept_type = accept_type
    self.queue_list = []
    self.on_task_list = []
    self.worker = Worker(self.conn, self.queue_list, self.on_task_list, self.accept_type)
    self.worker2 = Worker(self.conn, self.queue_list, self.on_task_list, self.accept_type)
    self.exchange_dict = {}
    self.get_exchange(self.exchange_name, self.exchange_type)

  def send_message(
      self,
      data: dict,
      routing_key: str,
      serializer: str = "json",
      exchange_name: str = None,
      exchange_type: str = None,
  ):
    print("ClueMQ send_message")
    exchange = self.get_exchange(exchange_name, exchange_type)
    res = self.worker.producer.publish(
        data,
        exchange=exchange,
        routing_key=routing_key,
        serializer=serializer
    )
    return res

  def run(self):
    print("ClueMQ run")
    self.worker.run()
    # t = threading.Thread(target=self.worker.run)
    # t.start()

  def setup_queue(self, routing_key, exchange_name=None, exchange_type=None):
    def decorator(func):
      self.add_queue(func, routing_key, exchange_name, exchange_type)
      return func
    return decorator

  @setup
  def add_queue(
        self,
        func,
        routing_key,
        exchange_name=None,
        exchange_type=None
    ):
    print("ClueMQ add_queue")
    queue_name = func.__name__
    exchange = self.get_exchange(exchange_name, exchange_type)
    queue = Queue(
        name=queue_name,
        exchange=exchange,
        routing_key=routing_key,
        durable=False
    )

    def on_task(body, message):
      try:
        result = func(**body)
        print(result)
      except Exception as exc:
        print("task raised exception: %r", exc)
      message.ack()

    self.queue_list.append(queue)
    self.on_task_list.append(on_task)
  
  def get_exchange(self, exchange_name, exchange_type):
    exchange_name = exchange_name or self.exchange_name
    exchange_type = exchange_type or self.exchange_type
    exchange = self.exchange_dict.get(exchange_name, None)
    if not exchange:
      exchange = Exchange(
          name=exchange_name,
          type=exchange_type,
          durable=True
      )
      self.exchange_dict[exchange_name] = exchange
    return exchange
