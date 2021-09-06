import threading

from kombu import Connection
from typing import List, Tuple

from clue_mq.exchange import ExchangeWrapper
from clue_mq.worker import Worker


class ClueMQ:
  def __init__(
      self,
      host: str = "localhost",
      exchange_list: List[Tuple[str, str]] = [
          ("cluemq", "topic")
      ],
      accept_type: str = "json"
  ):
    self.worker = Worker(Connection(host), accept_type)
    self.create_exchange(exchange_list)

  def create_exchange(self, exchange_list):
    for exchange_name, exchange_type in exchange_list:
      setattr(
          self,
          exchange_name,
          ExchangeWrapper(
              exchange_name,
              exchange_type,
              self.worker
          )
      )

  def run_subscribers(self):
    t = threading.Thread(target=self.worker.run)
    t.daemon = True
    t.start()
