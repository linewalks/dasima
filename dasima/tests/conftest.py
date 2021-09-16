import pytest


@pytest.fixture(scope="session")
def testmq():
  from flask import Flask
  from dasima import DasimaMQ

  app = Flask(__name__)
  app.config["DASIMA_EXCHANGE_SETTING"] = [("test_exchange", "topic")]
  testmq = DasimaMQ()
  testmq.init_app(app)

  return testmq
