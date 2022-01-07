import pytest
from dasima import Dasima


@pytest.fixture(scope="session")
def subscriber_1():
  from flask import Flask
  app = Flask(__name__)
  app.config["DASIMA_EXCHANGE_SETTING"] = [("test_type_one", "one"), ("test_type_all", "all")]
  return Dasima(app)


@pytest.fixture(scope="session")
def subscriber_2():
  from flask import Flask
  app = Flask(__name__)
  app.config["DASIMA_EXCHANGE_SETTING"] = [("test_type_one", "one"), ("test_type_all", "all")]
  return Dasima(app)


@pytest.fixture(scope="session")
def publisher():
  from flask import Flask
  app = Flask(__name__)
  app.config["DASIMA_EXCHANGE_SETTING"] = [("test_type_one", "one"), ("test_type_all", "all")]
  return Dasima(app)
