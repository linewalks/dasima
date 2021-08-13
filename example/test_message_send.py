import datetime
import os
import timeit
import sys
sys.path.append(os.getcwd())

from clue_mq import ClueMQ


cluemq = ClueMQ(
    host="localhost",
    exchange_name="clue",
    exchange_type="topic"
)


# serializer ex) "json", "pickle"...
def test_time():
    cluemq.send_message({"x": 3, "y": 3}, routing_key="clue.add", serializer="json")
    cluemq.send_message({"x": 3, "y": 3}, routing_key="clue.mul", serializer="json")
    cluemq.send_message({"x": 3, "y": 3}, routing_key="clue.div", serializer="json")


result = timeit.timeit(test_time, number=1000)
print(result)
