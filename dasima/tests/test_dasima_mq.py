import pytest
import time

from collections import Counter
from dasima import Dasima
from dasima.error import DasimaAlreadyRunError
from flask import Flask


class TestMQ:
  @pytest.fixture(scope="function")
  def number_list(self):
    yield []

  @pytest.fixture(scope="function")
  def subscriber(self, flask_app):
    return Dasima(flask_app)

  @pytest.fixture(scope="function")
  def run_subscribers(self, flask_app, number_list):
    dasima1 = Dasima(flask_app)
    dasima2 = Dasima(flask_app)

    @dasima1.test_type_one.subscribe("one")
    def test_func1():
      number_list.append(1)

    @dasima2.test_type_one.subscribe("one")
    def test_func2():
      number_list.append(2)

    @dasima1.test_type_all.subscribe("all")
    def test_func3():
      number_list.append(1)

    @dasima2.test_type_all.subscribe("all")
    def test_func4():
      number_list.append(2)

    dasima1.run_subscribers()
    dasima2.run_subscribers()

    yield

    dasima1.stop_subscribers()
    dasima2.stop_subscribers()

  @pytest.fixture(scope="function")
  def publisher(self, flask_app):
    return Dasima(flask_app)

  def test_init_app(self, flask_app):
    dasmia_1 = Dasima(flask_app)
    dasmia_2 = Dasima()
    dasmia_2.init_app(flask_app)
    assert dasmia_1.app == dasmia_2.app

  def test_run_subscribers_error(self, flask_app):
    dasmia = Dasima(flask_app)
    dasmia.run_subscribers()
    with pytest.raises(DasimaAlreadyRunError):
      dasmia.run_subscribers()
      dasima.stop_subscribers()

  def test_subscribe(self, subscriber):
    @subscriber.test_type_all.subscribe("test_routing_key")
    def test_exist_routing_key():
      return

    @subscriber.test_type_all.subscribe
    def test_not_exist_routing_key():
      return

    subscriber.run_subscribers()
    subscriber.stop_subscribers()

  @pytest.mark.parametrize("number", [2, 10, 100])
  def test_exchange_type_one_recive(self, publisher, number_list, number, run_subscribers):
    for i in range(number):
      publisher.test_type_one.send_message({}, "one")

    # Wait for received message to be processed
    time.sleep(number * 0.01)

    print(Counter(number_list))

  @pytest.mark.parametrize("number", [2, 10, 100])
  def test_exchange_type_one_recive(self, publisher, number_list, number, run_subscribers):
    for i in range(number):
      publisher.test_type_one.send_message({}, "one")

    # Wait for received message to be processed
    time.sleep(number * 0.01)

    counter = Counter(number_list)
    assert number // 2 == counter[1] == counter[2]

  @pytest.mark.parametrize("number", [2, 10, 100])
  def test_exchange_type_all_recive(self, publisher, number_list, number, run_subscribers):
    for i in range(number):
      publisher.test_type_all.send_message({}, "all")

    # Wait for received message to be processed
    time.sleep(number * 0.01)

    counter = Counter(number_list)
    assert number == counter[1] == counter[2]
