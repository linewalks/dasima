import pytest


@pytest.fixture(scope="session")
def exchange_setting_list():
  return [
      ("exchange_type_one", "one"),
      ("exchange_type_all", "all")
  ]


@pytest.fixture(scope="session")
def flask_app(exchange_setting_list):
  from flask import Flask
  app = Flask(__name__)
  app.config["DASIMA_EXCHANGE_SETTING"] = exchange_setting_list
  return app
