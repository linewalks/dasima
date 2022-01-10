import threading
import warnings

from kombu import Connection

from dasima.exchange import ExchangeWrapper
from dasima.worker import Worker
from dasima.error import DasimaAlreadyRunError


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
    self.connection = Connection(self.app.config.get("DASIMA_CONNECTION_HOST", "localhost"))
    self.connection.ensure_connection(max_retries=3)
    self.worker = Worker(
        connection=self.connection,
        accept_type=self.app.config.get("DASIMA_ACCEPT_TYPE", "json"),
        app_ctx=self.app_ctx
    )
    self.create_exchange()
    self.is_running = False

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
    if self.is_running:
      raise DasimaAlreadyRunError("run_subscribers is aleady running!")
    else:
      self.is_running = True
      self.setup_queue()
      t = threading.Thread(target=self.worker.run)
      t.daemon = True
      t.start()

      # worker가 준비가 될때 까지 잠시 기다려줌
      while True:
        if self.worker.is_ready:
          break
