import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from kombu import Connection, Exchange, Queue
from clue_mq import ClueMQ


cluemq = ClueMQ(
    host="localhost",
    exchange_name="clue",
    exchange_type="topic"
)
cluemq.connect()
cluemq.setup()
cluemq.close()
