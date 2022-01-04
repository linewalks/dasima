import uuid

from kombu import Exchange, Queue, binding
from flask.ctx import AppContext
from dasima.worker import Worker


class ExchangeWrapper:
  def __init__(
      self,
      exchange_name: str,
      exchange_type: str,
      worker: Worker
  ):
    self.exchange_type = exchange_type
    self.exchange = Exchange(
        name=exchange_name,
        type="topic",
        durable=True
    )
    self.__binding_dict = {}
    self.worker = worker

  def get_binding_dict(self):
    return self.__binding_dict

  def send_message(self, data, routing_key):
    self.worker.publish(
        data,
        self.exchange,
        routing_key
    )

  def subscribe(self, routing_key=None):
    if callable(routing_key):
      self.add_binding_dict(routing_key, None)
      return routing_key
    def decorator(func):
      self.add_binding_dict(func, routing_key)
      return func
    return decorator

  def add_binding_dict(self, func, routing_key):
    prefix = str(uuid.uuid4()) if self.exchange_type == "all" else ""
    key = prefix + self.exchange.name
    routing_key = func.__name__ if routing_key is None else routing_key

    if self.__binding_dict.get(key):
      self.__binding_dict[key].append((routing_key, func))
    else:
      self.__binding_dict[key] = [(routing_key, func)]
