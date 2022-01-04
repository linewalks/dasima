import gevent
import time
import pytest
import random


class TestMQ:
  @pytest.fixture(scope="class")
  def testmq(self):
    from flask import Flask
    from dasima import Dasima

    app = Flask(__name__)
    app.config["DASIMA_EXCHANGE_SETTING"] = [("test_exchange", "topic")]
    testmq = Dasima()
    testmq.init_app(app)

    return testmq

  @pytest.fixture(scope="class")
  def test_cnt(self):
    value = {
        "cnt": 0,
        "load_cnt": 0
    }
    yield value

  def test_subscribe(self, testmq, test_cnt):
    @testmq.test_exchange.subscribe("test")
    def test_func(x, y):
      test_cnt["cnt"] += 1
      return x + y

    @testmq.test_exchange.subscribe("load")
    def test_load_func(x, y):
      test_cnt["load_cnt"] += 1
      return x + y

    testmq.run_subscribers()

  def test_message_send_and_recevie(self, testmq, test_cnt):
    number = random.randint(1, 1000)
    for i in range(number):
      testmq.test_exchange.send_message({"x": 3, "y": 3}, "test")

    # Wait for received message to be processed
    time.sleep(number * 0.01)
    assert number == test_cnt["cnt"]

  def test_multi_heavy_load(self, testmq, test_cnt):
    def send():
      for _ in range(100):
        testmq.test_exchange.send_message({"x": 3, "y": 3}, "load")

    gevent.joinall([gevent.spawn(send) for _ in range(100)])

    # Wait for received message to be processed
    time.sleep(10)

    assert test_cnt["load_cnt"] == 100 * 100
