import pytest


@pytest.fixture(scope="session")
def testmq():
  from clue_mq import ClueMQ
  testmq = ClueMQ(
      host="localhost",
      exchange_list=[("test_exchange", "topic")]
  )

  return testmq
