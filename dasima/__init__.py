import threading

from kombu import Connection
from typing import List, Tuple

from dasima.exchange import ExchangeWrapper
from dasima.worker import Worker


class Dasima:
  def __init__(self, app=None):
    self.app = app
    if app:
      self.init_app(app)

  def init_app(self, app):
    self.app = app
    self.app_ctx = self.app.app_context()
    self.exchange_list = self.app.config.get(
        "DASIMA_EXCHANGE_SETTING",
        [("dasima_test", "one")]
    ) 
    self.worker = Worker(
        connection=Connection(self.app.config.get("DASIMA_CONNECTION_HOST", "localhost")),
        accept_type=self.app.config.get("DASIMA_ACCEPT_TYPE", "json"),
        app_ctx=self.app_ctx
    )
    self.create_exchange()

  def create_exchange(self):
    for exchange_name, exchange_type in self.exchange_list:
      setattr(
          self,
          exchange_name,
          ExchangeWrapper(
              exchange_name,
              exchange_type,
              self.worker
          )
      )

  def setup_queue(self):
    for exchange_name, exchange_type in self.exchange_list:
      exchange = getattr(
          self,
          exchange_name
      )
      self.worker.add_consumer_config_list(exchange)

  def run_subscribers(self):
    self.setup_queue()
    t = threading.Thread(target=self.worker.run)
    t.daemon = True
    t.start()
