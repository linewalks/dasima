import time
import threading

from functools import update_wrapper
from typing import Callable

from flask import g
from kombu import Connection

from dasima.exchange import ExchangeWrapper


__version__ = "1.0.1"


def setupmethod(f):
  def wrapper_func(self, *args, **kwargs):
    return f(self, *args, **kwargs)
  return update_wrapper(wrapper_func, f)


class Dasima:
  def __init__(self, app=None):
    self.app = app
    self.__after_task_list = []
    if app:
      self.init_app(app)

  def init_app(self, app):
    self.app = app

    @app.teardown_appcontext
    def close_connection(error):
      if hasattr(g, "_dasima_connection"):
        g._dasima_connection.close()

    self.exchange_setting_list = self.app.config.get(
        "DASIMA_EXCHANGE_SETTING",
        [("dasima_test", "one")]
    )
    self.connection = Connection(self.app.config.get("DASIMA_CONNECTION_HOST", "localhost"))

    self.register_exchange()
    self.is_running = False

  @setupmethod
  def after_subscribe_task(self, f):
    self.register_after_subscribe_task(f)

  def register_after_subscribe_task(self, func: Callable):
    self.__after_task_list.append(func)

  def register_exchange(self):
    for exchange_name, exchange_type in self.exchange_setting_list:
      setattr(
          self,
          exchange_name,
          ExchangeWrapper(
              self.app,
              self.connection,
              exchange_name,
              exchange_type,
              self.__after_task_list
          )
      )

    self.exchange_list = [
        getattr(self, exchange_name)
        for exchange_name, _ in self.exchange_setting_list
    ]

  def run_subscribers(self):
    if self.is_running:
      raise RuntimeError("run_subscribers is aleady running!")
    else:
      self.is_running = True
      for exchange in self.exchange_list:
        t = threading.Thread(target=exchange.run, daemon=True)
        t.start()
      # worker가 준비가 될때 까지 잠시 기다려줌
      while True:
        if all([
            exchange.is_ready
            for exchange in self.exchange_list
        ]):
          break
        time.sleep(0.01)

  def stop_subscribers(self):
    for exchange in self.exchange_list:
      exchange.stop()
