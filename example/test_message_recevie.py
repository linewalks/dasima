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

@cluemq.setup_queue("clue.add", "clue")
def add(x, y):
  return x + y

@cluemq.setup_queue("clue.mul", "clue")
def mul(x, y):
  return x * y


def div(x, y):
  return x // y


if __name__ == "__main__":
  cluemq.add_queue(div, "clue.div", "clue")
  cluemq.run()
