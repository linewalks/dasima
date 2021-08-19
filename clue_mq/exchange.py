from kombu import Exchange, Queue

from clue_mq.worker import Worker

class ExchangeWrapper:
  def __init__(
      self,
      exchange_name: str,
      exchange_type: str,
      worker: Worker
  ):
    self.worker = worker
    self.exchange = Exchange(
        name=exchange_name,
        type=exchange_type,
        durable=True
    )

  def send_message(self, data, routing_key):
    self.worker.publish(
        data,
        self.exchange,
        routing_key
    )

  def subscribe(self, routing_key):
    def decorator(func):
      self.add_consumer_config(func, routing_key)
      return func
    return decorator

  def add_consumer_config(
      self,
      func,
      routing_key
  ):
    queue_name = func.__name__
    queue = Queue(
        name=queue_name,
        exchange=self.exchange,
        routing_key=routing_key,
        durable=True
    )

    def on_task(body, message):
      try:
        func(**body)
      finally:
        message.ack()

    self.worker.add_consumer_config(queue, on_task)
