from flask import g
from kombu import (
    uuid,
    Connection,
    Consumer,
    Producer,
    Queue
)


class CallbackResponse:
  def __init__(self):
    self.response = None


class ProducerWorker:
  def __init__(
      self,
      connection: Connection,
      accept_type: str
  ):
    self._connection = connection
    self.accept_type = accept_type

  @property
  def connection(self):
    if hasattr(g, "_dasima_connection"):
      return g._dasima_connection
    g._dasima_connection = self._connection.clone()
    g._dasima_connection.ensure_connection(max_retries=1)
    return g._dasima_connection

  def send_message(
      self,
      data,
      routing_key,
      exchange,
      callback_queue=None
  ):
    with Producer(self.connection) as producer:
      producer.publish(
          body=data,
          exchange=exchange,
          routing_key=routing_key,
          serializer=self.accept_type,
          declare=[callback_queue] if callback_queue else None,
          reply_to=callback_queue.name if callback_queue else None
      )

  def call(self, data, routing_key, exchange, timeout=5):
    callback = CallbackResponse()
    callback_uuid = uuid()

    def on_response(message):
      callback.response = message.payload["result"]

    callback_queue = Queue(
        name=callback_uuid,
        exchange=exchange,
        routing_key=callback_uuid,
        exclusive=True,
        auto_delete=True
    )

    self.send_message(
        data,
        routing_key,
        exchange,
        callback_queue=callback_queue
    )

    with Consumer(
        self.connection,
        on_message=on_response,
        queues=[callback_queue],
        no_ack=True
    ):
      while callback.response is None:
        self.connection.drain_events(timeout=timeout)

    return callback.response
