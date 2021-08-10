import os
import sys
sys.path.append(os.getcwd())

from clue_mq import ClueMQ


cluemq = ClueMQ(
    host="localhost",
    exchange_name="clue",
    exchange_type="topic"
)


def add(x, y):
  return x + y


def mul(x, y):
  return x * y


def div(x, y):
  return x // y


if __name__ == "__main__":

  cluemq.add_queue("clue.add", add, "clue")
  cluemq.add_queue("clue.mul", mul, "clue")
  cluemq.add_queue("clue.div", div, "clue")
  cluemq.run()
