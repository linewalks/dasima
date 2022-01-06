import pytest
from dasima import Dasima


@pytest.fixture(scope="session")
def subscriber_1():
  from flask import Flask
  app = Flask(__name__)
  app.config["DASIMA_EXCHANGE_SETTING"] = [("test_type_one", "one"), ("test_type_all", "all")]
  subscriber_1 = Dasima(app)
  return subscriber_1


@pytest.fixture(scope="session")
def subscriber_2():
  from flask import Flask
  app = Flask(__name__)
  app.config["DASIMA_EXCHANGE_SETTING"] = [("test_type_one", "one"), ("test_type_all", "all")]
  subscriber_2 = Dasima()
  subscriber_2.__init__(app)
  return subscriber_2


@pytest.fixture(scope="session")
def publisher():
  from flask import Flask
  app = Flask(__name__)
  app.config["DASIMA_EXCHANGE_SETTING"] = [("test_type_one", "one"), ("test_type_all", "all")]
  publisher = Dasima()
  publisher.__init__(app)
  return publisher
