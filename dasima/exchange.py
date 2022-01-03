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
    self.exchange_name = exchange_name
    self.exchange = Exchange(
        name=exchange_name,
        type=exchange_type,
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

  def subscribe(self, arg=None):
    if callable(arg):
      self.add_binding_dict(arg, None)
      return arg
    def decorator(func):
      self.add_binding_dict(func, arg)
      return func
    return decorator

  def add_binding_dict(self, func, routing_key):
    key = self.exchange_name
    routing_key = func.__name__ if routing_key is None else routing_key

    if self.__binding_dict.get(key):
      self.__binding_dict[key].append((routing_key, func))
    else:
      self.__binding_dict[key] = [(routing_key, func)]
