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
    print("__dasima__init__")
    self.app = app
    self.app_ctx = self.app.app_context()
    self.worker = Worker(
        connection=Connection(
            self.app.config.get("DASIMA_CONNECTION_HOST", "localhost")
        ),
        accept_type=self.app.config.get("DASIMA_ACCEPT_TYPE", "json")
    )
    self.create_exchange(
        exchange_list=self.app.config.get(
            "DASIMA_EXCHANGE_SETTING",
            [("dasima_test", "topic")]
        )
    )

  def create_exchange(self, exchange_list):
    print("__dasima__create_exchange__")
    for exchange_name, exchange_type in exchange_list:
      setattr(
          self,
          exchange_name,
          ExchangeWrapper(
              exchange_name,
              exchange_type,
              self.app_ctx,
              self.worker
          )
      )

  def run_subscribers(self):
    print("__dasima__run_subscribers__")
    t = threading.Thread(target=self.worker.run)
    t.daemon = True
    t.start()
