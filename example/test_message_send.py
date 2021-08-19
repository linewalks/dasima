import datetime
import os
import timeit
import sys
sys.path.append(os.getcwd())

from clue_mq import ClueMQ


cluemq = ClueMQ(
    host="localhost",
    exchange_list=[("clue", "topic"), ("login", "topic")],
)


def test_time():
  cluemq.clue.send_message({"x": 3, "y": 3}, "add")
  cluemq.clue.send_message({"x": 3, "y": 3}, "mul")
  cluemq.login.send_message({"x": 3, "y": 3}, "div")
  cluemq.login.send_message({"x": 3, "y": 3}, "sub")


result = timeit.timeit(test_time, number=1000)
print(result)
