import pytest
import time

from dasima import Dasima
from dasima.error import DasimaAlreadyRunError
from flask import Flask


class TestMQ:
  @pytest.fixture(scope="class")
  def count(self):
    value = {
        "one_cnt_1": 0,
        "one_cnt_2": 0,
        "all_cnt": 0
    }
    yield value

  @pytest.fixture(scope="function")
  def subscriber_1(self, flask_app):
    return Dasima(flask_app)

  @pytest.fixture(scope="function")
  def subscriber_2(self, flask_app):
    return Dasima(flask_app)

  @pytest.fixture(scope="function")
  def publisher(self, flask_app):
    return Dasima(flask_app)

  def test_init_app(self):
    app = Flask("test")
    dasmia_1 = Dasima(app)
    dasmia_2 = Dasima()
    dasmia_2.init_app(app)
    assert dasmia_1.app == dasmia_2.app

  def test_run_subscribers_warning(self):
    app = Flask("test")
    dasmia = Dasima(app)
    dasmia.run_subscribers()
    with pytest.raises(DasimaAlreadyRunError):
      dasmia.run_subscribers()

  def test_subscribe(self, subscriber_1):
    @subscriber_1.test_type_one.subscribe("test_routing_key")
    def test_exist_routing_key():
      return

    @subscriber_1.test_type_all.subscribe
    def test_not_exist_routing_key():
      return

    subscriber_1.run_subscribers()

  # @pytest.mark.parametrize("number", [2, 10, 100])
  # def test_exchange_type_one_recive(self, publisher, count, number):
  #   for i in range(number):
  #     publisher.test_type_one.send_message({}, "one")

  #   # Wait for received message to be processed
  #   time.sleep(number * 0.01)

  #   assert count["one_cnt_1"] == number // 2
  #   assert count["one_cnt_2"] == number // 2
  #   # init count
  #   count["one_cnt_1"] = 0
  #   count["one_cnt_2"] = 0

  # @pytest.mark.parametrize("number", [2, 10, 100])
  # def test_exchange_type_all_recive(self, publisher, count, number):
  #   for i in range(number):
  #     publisher.test_type_all.send_message({}, "test_all_func")

  #   # Wait for received message to be processed
  #   time.sleep(number * 0.01)

  #   assert count["all_cnt"] == number * 2

  #   count["all_cnt"] = 0
