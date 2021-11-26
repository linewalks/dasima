import random
import string

from kombu import Exchange, Queue
from flask.ctx import AppContext
from dasima.worker import Worker


RANDOM_STRING = string.ascii_letters + string.digits
LENGTH = 6


class ExchangeWrapper:
  def __init__(
      self,
      exchange_name: str,
      exchange_type: str,
      app_ctx: AppContext,
      worker: Worker
  ):
    self.worker = worker
    self.app_ctx = app_ctx
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
      self.add_consumer_config(func, routing_key, False)
      return func
    return decorator

  def multi_subscribe(self, routing_key):
    def decorator(func):
      self.add_consumer_config(func, routing_key, True)
      return func
    return decorator

  def add_consumer_config(
      self,
      func,
      routing_key,
      is_multi
  ):
    suffix = ''.join(random.choices(RANDOM_STRING, k=LENGTH)) if is_multi else ""
    queue_name = func.__name__ + suffix
    queue = Queue(
        name=queue_name,
        exchange=self.exchange,
        routing_key=routing_key,
        durable=True,
        auto_delete=is_multi
    )

    def on_task(body, message):
      try:
        self.app_ctx.push()
        func(**body)
      finally:
        message.ack()
        self.app_ctx.pop()

    self.worker.add_consumer_config(queue, on_task)
