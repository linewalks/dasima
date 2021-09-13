import pytest


@pytest.fixture(scope="session")
def testmq():
  from dasima import DasimaMQ
  testmq = DasimaMQ(
      host="localhost",
      exchange_list=[("test_exchange", "topic")]
  )

  return testmq
