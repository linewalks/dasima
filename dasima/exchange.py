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
  
  def subscribe(self, queue, routing_key):
    def decorator(func):
      self.add_binding_dict(queue, routing_key, func)
      return func
    return decorator
  
  def add_binding_dict(self, queue, routing_key, func):
    if self.__binding_dict.get(queue):
      self.__binding_dict[queue].append((routing_key, func))
    else:
      self.__binding_dict[queue] = [(routing_key, func)]
