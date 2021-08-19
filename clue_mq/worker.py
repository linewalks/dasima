from kombu import Connection, Consumer
from kombu.mixins import ConsumerProducerMixin


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
      accept_type: str,
  ):
    self.connection = connection
    self.consumer_config_list = []
    self.accept_type = accept_type
    self.channel_list = []

  def close_channels(self):
    for channel in self.channel_list:
      # TODO maybe_close_channel
      if channel:
        channel.close()

  # kombu의 각각에 Channel에 독립적인 threading을 적용 하기 전
  # 사전 작업 으로 각자의 Consumer마다 channel을 할당
  def get_consumers(self, _, default_channel):

    # TODO get_consumers 호출 마다 새로운 Connection을 연결해 주기에
    # 기존에 연결 되어 있는 Connection을 닫아 줘야 되지만
    # 현재 Connection.close 시 socket.timeout: timed out 에러 발생으로 원인 조사중
    self.close_channels()

    channel_list = [default_channel]
    channel_list.extend([
        default_channel.connection.channel()
        for _ in range(len(self.consumer_config_list) - 1)
    ])
    self.channel_list = channel_list

    return [
        Consumer(
            channel=channel,
            queues=[queue],
            accept=[self.accept_type],
            callbacks=[on_task]
        )
        for channel, (queue, on_task) in zip(self.channel_list, self.consumer_config_list)
    ]

  # connection으로 channel들을 불러온다.
  def on_consume_end(self, connection, default_channel):
    self.close_channels()

  def publish(self, data, exchange, routing_key):
    self.producer.publish(
        body=data,
        exchange=exchange,
        routing_key=routing_key,
        serializer=self.accept_type
    )

  def add_consumer_config(self, queue, on_task):
    self.consumer_config_list.append((queue, on_task))
