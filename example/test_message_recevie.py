import os
import sys
sys.path.append(os.getcwd())

from clue_mq import ClueMQ


cluemq = ClueMQ(
    host="localhost",
    exchange_name="clue",
    exchange_type="topic",
    accept_type=["json", "pickle"]
)

@cluemq.subscribe(routing_key="clue.add")
def add(x, y):
  return x + y


@cluemq.subscribe(routing_key="clue.mul")
def mul(x, y):
  return x * y


@cluemq.subscribe(routing_key="clue.div")
def div(x, y):
  return x // y


if __name__ == "__main__":
  cluemq.run_subscribers()
