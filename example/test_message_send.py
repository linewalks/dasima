import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from clue_mq import ClueMQ


cluemq = ClueMQ(
    host="localhost",
    exchange_name="clue",
    exchange_type="topic"
)

# serializer ex) "json", "pickle"...
cluemq.send_message({"x": 3, "y": 3}, routing_key="clue.add", serializer="json")
cluemq.send_message({"x": 3, "y": 3}, routing_key="clue.mul", serializer="json")
cluemq.send_message({"x": 3, "y": 3}, routing_key="clue.div", serializer="json")
