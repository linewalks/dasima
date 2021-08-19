import os
import sys
sys.path.append(os.getcwd())

from clue_mq import ClueMQ


cluemq = ClueMQ(
    host="localhost",
    exchange_list=[("clue", "topic"), ("login", "topic")]
)

@cluemq.clue.subscribe("add")
def add(x, y):
  print("ADD", x, y)
  return x + y


@cluemq.clue.subscribe("mul")
def mul(x, y):
  print("MUL", x, y)
  return x * y


@cluemq.login.subscribe("div")
def div(x, y):
  print("DIV", x, y)
  return x // y


@cluemq.login.subscribe("sub")
def sub(x, y):
  print("SUB", x, y)
  return x - y


if __name__ == "__main__":
  cluemq.run_subscribers()
