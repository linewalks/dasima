import time

from kombu import Connection, Consumer
from kombu.mixins import ConsumerMixin


class ConsumerWorker(ConsumerMixin):
  """
  kombu 라이브러리의 ConsumerMixin 상속 하여 Consumer 기능을 쉽게 사용
  해당 클래스의 run 함수 호출 시 Consumer 기능 활성화
  """
  def __init__(
      self,
      connection: Connection,
      accept_type: str,
  ):
    self.connection = connection
    self.accept_type = accept_type
    self.channel_list = []
    self.__consumer_config_list = []
    self.is_ready = False

  def close_channels(self):
    for channel in self.channel_list:
      # TODO maybe_close_channel
      if channel:
        channel.close()

  def on_consume_ready(self, connection, channel, consumers, **kwargs):
    self.is_ready = True

  def add_consumer_config(self, queue, on_task):
    self.__consumer_config_list.append((queue, on_task))

  # 사전 작업 으로 각자의 Consumer마다 channel을 할당
  def get_consumers(self, _, default_channel):
    channel_list = [default_channel]
    channel_list.extend([
        default_channel.connection.channel()
        for _ in range(len(self.__consumer_config_list) - 1)
    ])
    self.channel_list = channel_list

    return [
        Consumer(
            channel=channel,
            queues=[queue],
            accept=[self.accept_type],
            callbacks=[on_task]
        )
        for channel, (queue, on_task) in zip(self.channel_list, self.__consumer_config_list)
    ]

  # connection으로 channel들을 불러온다.
  def on_consume_end(self, connection, default_channel):
    self.close_channels()

  def stop(self):
    self.should_stop = True
    self.connection.release()
