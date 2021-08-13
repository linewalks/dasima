import threading
from typing import List
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerProducerMixin

from clue_mq.utils import setup


# The basic class ConsumerMixin would need a :attr:`connection` attribute
# which must be a :class:`~kombu.Connection` instance,
# and define a :meth:`get_consumers` method that returns a list of :class:`kombu.Consumer` instances to use.
class Worker(ConsumerProducerMixin):
  """
  Woker class는 함수를 kombu 라이브러리의 ConsumerProducerMixin을 상속 받아
  kombu의 publisher, consumer의 기능을 사용하기 쉽게 지원을 해줍니다.
  publisher: producer 호출시 Worker connetion을 클론 받는 Producer를 리턴 해줌
  consumer: run 함수 실행 시 get_consumers 함수가 호출되며 consumer_config 값에 설정된 라우팅 큐에 해당 되는 메세지 큐을 구독하는 Comsumer 생성
  """
  def __init__(
      self,
      connection: Connection,
      accept_type: List[str],
  ):
    self.connection = connection
    self.consumer_config_list = []
    self.accept_type = accept_type

  def get_consumers(self, Consumer, channel):
    return [
        Consumer(
            queues=[queue],
            accept=self.accept_type,
            callbacks=[on_task]
        )
        for queue, on_task in self.consumer_config_list
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
    self.accept_type = accept_type
    self.worker = Worker(self.conn, self.accept_type)
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
    exchange = self.get_exchange(exchange_name, exchange_type)
    self.worker.producer.publish(
        data,
        exchange=exchange,
        routing_key=routing_key,
        serializer=serializer
    )

  def run_subscribers(self):
    t = threading.Thread(target=self.worker.run)
    t.start()

  def subscribe(self, routing_key, exchange_name=None, exchange_type=None):
    def decorator(func):
      self.add_consumer_config(func, routing_key, exchange_name, exchange_type)
      return func
    return decorator

  @setup
  def add_consumer_config(
      self,
      func,
      routing_key,
      exchange_name=None,
      exchange_type=None
  ):
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

    self.worker.consumer_config_list.append((queue, on_task))

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
