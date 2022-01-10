import pytest
from dasima import Dasima


@pytest.fixture(scope="session")
def flask_app():
  from flask import Flask
  app = Flask(__name__)
  app.config["DASIMA_EXCHANGE_SETTING"] = [("test_type_one", "one"), ("test_type_all", "all")]
  return app
