from flask.app import Flask
from kombu import Connection, Consumer, Producer, Queue, uuid


class RpcClient:
  def __init__(
      self,
      app: Flask
  ):
    self.connection = Connection(app.config.get("DASIMA_CONNECTION_HOST", "localhost"))
    self.connection.ensure_connection(max_retries=3)

  def on_response(self, message):
    if message.properties["correlation_id"] == self.correlation_id:
      self.response = message.payload["result"]

  def call(self, data, routing_key, exchange):
    self.response = None
    self.correlation_id = uuid()
    self.const_uuid = uuid()

    self.callback_queue = Queue(
        name=self.const_uuid,
        exchange=exchange,
        routing_key=self.const_uuid,
        exclusive=True,
        auto_delete=True
    )
    with Producer(self.connection) as producer:
      producer.publish(
          data,
          exchange=exchange,
          routing_key=routing_key,
          declare=[self.callback_queue],
          reply_to=self.callback_queue.name,
          correlation_id=self.correlation_id,
      )

    with Consumer(
        self.connection,
        on_message=self.on_response,
        queues=[self.callback_queue],
        no_ack=True
    ):
      while self.response is None:
        self.connection.drain_events(timeout=10)

    self.connection.close()

    return self.response
