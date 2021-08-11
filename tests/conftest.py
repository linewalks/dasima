import pytest
import os
import sys
sys.path.append(os.getcwd())


@pytest.fixture(scope="module")
def cluemq():
  from clue_mq import ClueMQ
  cluemq = ClueMQ(
      host="localhost",
      exchange_name="test",
      exchange_type="topic"
  )
  return cluemq

@pytest.fixture(scope="module")
def Coneection(cluemq):
  with cluemq.connection:
    yield
