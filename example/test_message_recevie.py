import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from clue_mq import ClueMQ

cluemq = ClueMQ(
    host="localhost",
    exchange_name="clue",
    queue_name="generator",
    queue_routing_key="clue.generator",
    exchange_type="topic"
)

if __name__ == "__main__":
  cluemq.run()