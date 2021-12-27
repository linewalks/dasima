from kombu import Exchange, Queue
from flask.ctx import AppContext
from dasima.worker import Worker


class ExchangeWrapper:
  def __init__(
      self,
      exchange_name: str,
      exchange_type: str,
      app_ctx: AppContext,
      worker: Worker
  ):
    print("__exchangerwrapper_init__")
    self.worker = worker
    self.app_ctx = app_ctx
    self.exchange = Exchange(
        name=exchange_name,
        type=exchange_type,
        durable=True
    )

  def send_message(self, data, routing_key):
    print("__exchangerwrapper_send_message__")
    self.worker.publish(
        data,
        self.exchange,
        routing_key
    )

  def subscribe(self, routing_key):
    print(f"__exchangerwrapper_subscribe_{routing_key}__")
    def decorator(func):
      self.add_consumer_config(func, routing_key)
      return func
    return decorator

  def add_consumer_config(
      self,
      func,
      routing_key
  ):
    print("__exchangerwrapper_add_consumer__")
    queue_name = func.__name__
    queue = Queue(
        name=queue_name,
        exchange=self.exchange,
        routing_key=routing_key,
        durable=True
    )

    def on_task(body, message):
      try:
        self.app_ctx.push()
        func(**body)
      finally:
        message.ack()
        self.app_ctx.pop()

    self.worker.add_consumer_config(queue, on_task)
