from typing import Callable, List
from collections import defaultdict
from flask.app import Flask
from kombu import (
    binding,
    uuid,
    Connection,
    Exchange,
    Queue
)

from dasima.consumer import ConsumerWorker
from dasima.producer import ProducerWorker


class ExchangeWrapper:
  def __init__(
      self,
      app: Flask,
      connection: Connection,
      exchange_name: str,
      exchange_type: str,
      after_task_list: List[Callable]
  ):
    self.app = app
    self.exchange_type = exchange_type
    self.exchange = Exchange(
        name=exchange_name,
        type="topic",
        durable=True
    )
    self.__binding_dict = defaultdict(list)
    self._connection = connection
    self.accept_type = self.app.config.get("DASIMA_ACCEPT_TYPE", "json")
    self.producer_worker = ProducerWorker(
        connection=self._connection,
        accept_type=self.accept_type
    )
    self.consumer_worker = ConsumerWorker(
        connection=self._connection.clone(),
        accept_type=self.accept_type,
    )
    self.after_task_list = after_task_list
    self.register_rpc_send_message()

  @property
  def is_ready(self):
    return self.consumer_worker.is_ready

  def register_rpc_send_message(self):
    if self.exchange_type == "one":
      setattr(
          self,
          "send_message_and_recevie_result",
          self.__send_message_and_recevie_result
      )

  def get_binding_dict(self):
    return self.__binding_dict

  def send_message(self, data, routing_key):
    self.producer_worker.send_message(data, routing_key, self.exchange)

  def __send_message_and_recevie_result(self, data, routing_key, timeout=5):
    try:
      return self.producer_worker.call(data, routing_key, self.exchange, timeout)
    except Exception as err:
      """
      BackLog: 추가적인 에러 처리 필요
      에러 발생시 클라이언트에서 지장이 없도록 None으로 반환
      """
      print(err)
      return None

  def add_binding_dict(self, func, routing_key):
    if self.exchange_type == "all":
      queue_name = f"{self.exchange.name}-{uuid()}"  # Kombu uuid same as str(uuid4)
    else:
      queue_name = self.exchange.name

    routing_key = func.__name__ if routing_key is None else routing_key

    self.__binding_dict[queue_name].append((routing_key, func))

  def subscribe(self, routing_key=None):
    if callable(routing_key):
      self.add_binding_dict(routing_key, None)
      return routing_key

    def decorator(func):
      self.add_binding_dict(func, routing_key)
      return func

    return decorator

  def add_config_consumer_worker(self, queue, on_task):
    self.consumer_worker.add_consumer_config(queue, on_task)

  def make_combine_function(self, func_list):
    def func(data, routing_key):
      func_dict = dict(func_list)
      if func_dict.get(routing_key):
        return func_dict[routing_key](**data)
    return func

  def register_consumer_queue(self):
    auto_delete = True if self.exchange_type == "all" else False
    for queue_name, bind_list in self.__binding_dict.items():
      func = self.make_combine_function(bind_list)
      bindings = [
          binding(self.exchange, routing_key=routing_key)
          for routing_key, _ in bind_list
      ]

      def on_task(body, message):
        routing_key = message.delivery_info["routing_key"]
        with self.app.app_context():
          try:
            if func is not None:
              result = func(body, routing_key)
              if message.properties.get("reply_to"):
                self.producer_worker.send_message(
                    {"result": result},
                    exchange=self.exchange,
                    routing_key=message.properties["reply_to"]
                )
          finally:
            message.ack()

          for after_task in self.after_task_list:
            after_task(body, message, result)

      queue = Queue(
          name=queue_name,
          exchange=self.exchange,
          bindings=bindings,
          durable=True,
          auto_delete=auto_delete
      )
      self.add_config_consumer_worker(queue, on_task)

  def run(self):
    self.register_consumer_queue()
    self.consumer_worker.run()

  def stop(self):
    self.consumer_worker.stop()
