import os
import sys
sys.path.append(os.getcwd())

import pytest


@pytest.fixture(scope="session")
def cluemq():
  from clue_mq import ClueMQ
  cluemq = ClueMQ(
      host="localhost",
      exchange_name="test",
      exchange_type="topic"
  )
  return cluemq
