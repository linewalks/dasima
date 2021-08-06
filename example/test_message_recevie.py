import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

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
  return x//y


if __name__ == "__main__":
  cluemq.add_queue("clue", "clue.add", add)
  cluemq.add_queue("clue", "clue.mul", mul)
  cluemq.add_queue("clue", "clue.div", div)
  cluemq.run()
