import pytest
import random
import time

from dasima import Dasima
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

  def test_init_app(self):
    app = Flask("test")
    dasmia_1 = Dasima(app)
    dasmia_2 = Dasima()
    dasmia_2.init_app(app)
    assert dasmia_1.app == dasmia_2.app

  def test_subscribe(self, subscriber_1, subscriber_2, count):
    @subscriber_1.test_type_one.subscribe("one")
    def test_one_func1():
      count["one_cnt_1"] += 1
      return

    @subscriber_2.test_type_one.subscribe("one")
    def test_one_func2():
      count["one_cnt_2"] += 1
      return

    # when there is not routing key, routing key is set automatically function name
    @subscriber_1.test_type_all.subscribe
    @subscriber_2.test_type_all.subscribe
    def test_all_func():
      count["all_cnt"] += 1
      return

    subscriber_1.run_subscribers()
    subscriber_2.run_subscribers()

  @pytest.mark.parametrize("number", [2, 10, 100])
  def test_exchange_type_one_recive(self, publisher, count, number):
    for i in range(number):
      publisher.test_type_one.send_message({}, "one")

    # Wait for received message to be processed
    time.sleep(number * 0.01)

    assert count["one_cnt_1"] == number // 2
    assert count["one_cnt_2"] == number // 2
    # init count
    count["one_cnt_1"] = 0
    count["one_cnt_2"] = 0

  @pytest.mark.parametrize("number", [2, 10, 100])
  def test_exchange_type_all_recive(self, publisher, count, number):
    for i in range(number):
      publisher.test_type_all.send_message({}, "test_all_func")

    # Wait for received message to be processed
    time.sleep(number * 0.01)

    assert count["all_cnt"] == number * 2

    count["all_cnt"] = 0
