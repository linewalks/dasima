import threading

from kombu import Connection, Consumer, Exchange, Queue
from kombu.mixins import ConsumerProducerMixin
from typing import List

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
    self.channel_list = []

  # kombu의 각각에 Channel에 독립적인 threading을 적용 하기 전
  # 사전 작업 으로 각자의 Consumer마다 channel을 할당
  # worker.run 실행 될때만 호출이 된다. 중복으로 호출될 경우가 있을까??
  def get_consumers(self, _, default_channel):

    # TODO get_consumers 호출 마다 새로운 Connection을 연결해 주기에
    # 기존에 연결 되어 있는 Connection을 닫아 줘야 되지만
    # 현재 Connection.close 시 socket.timeout: timed out 에러 발생으로 원인 조사중
    for channel in self.channel_list:
      if channel:
        channel.close()

    channel_list = []
    channel_list.append(default_channel)
    channel_list.extend([
        default_channel.connection.channel()
        for _ in range(len(self.consumer_config_list) - 1)
    ])
    self.channel_list = channel_list

    return [
        Consumer(
            channel=channel,
            queues=[config[0]],
            accept=self.accept_type,
            callbacks=[config[1]]
        )
        for channel, config in zip(self.channel_list, self.consumer_config_list)
    ]

  def on_consume_end(self, connection, default_channel):
    for channel in self.channel_list:
      if channel:
        channel.close()


class ClueMQ:
  """
  CLUE MQ는
  @subscribe 데코레이터를 지정한 함수를 원하는 라우팅 키를 사용하여
  구독을 하는 기능을 지원 합니다. 
  또한 send_message 함수를 사용하여 지정된 라우팅 키로 원하는 데이터를
  메세지로 보낼수 있습니다.
  """
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
        body=data,
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
