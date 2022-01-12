import pytest
import time

from collections import Counter
from dasima import Dasima


class TestDasimaSetup:
  def test_init_app(self, flask_app):
    dasmia1 = Dasima(flask_app)
    dasmia2 = Dasima()
    dasmia2.init_app(flask_app)
    assert dasmia1.app == dasmia2.app

  def test_create_exchange(self, exchange_setting_list, flask_app):
    dasima = Dasima(flask_app)
    for exchange_name, exchange_type in exchange_setting_list:
      exchange = getattr(dasima, exchange_name)
      assert exchange.exchange_type == exchange_type
      assert exchange.exchange.name == exchange_name


class TestDasimaSubscribe:
  @pytest.fixture(scope="function")
  def dasima(self, flask_app):
    return Dasima(flask_app)

  def test_subscribe_exist_routing_key(self, dasima):
    @dasima.exchange_type_one.subscribe("test")
    def test_func():
      return

    binding_dict = dasima.exchange_type_one.get_binding_dict()
    routing_key, _ = binding_dict["exchange_type_one"][0]
    assert routing_key == "test"

  def test_subscribe_not_exist_routing_key(self, dasima):
    @dasima.exchange_type_one.subscribe
    def test_func():
      return

    binding_dict = dasima.exchange_type_one.get_binding_dict()
    routing_key, _ = binding_dict["exchange_type_one"][0]
    assert routing_key == "test_func"

  def test_run_subscribers_error(self, dasima):
    dasima.run_subscribers()
    with pytest.raises(RuntimeError):
      dasima.run_subscribers()


class TestDasimaMessageSendReceive:
  @pytest.fixture(scope="function")
  def count_list(self):
    yield []

  @pytest.fixture(scope="function")
  def dasima1(self, flask_app):
    return Dasima(flask_app)

  @pytest.fixture(scope="function")
  def dasima2(self, flask_app):
    return Dasima(flask_app)

  @pytest.fixture(scope="function")
  def publisher(self, flask_app):
    return Dasima(flask_app)

  @pytest.mark.parametrize("number", [2, 10, 100])
  def test_exchange_type_one_recive(self, dasima1, dasima2, publisher, number, count_list):

    @dasima1.exchange_type_one.subscribe("one")
    def test_subscribe_function_1():
      count_list.append(1)
      return

    @dasima2.exchange_type_one.subscribe("one")
    def test_subscribe_function_2():
      count_list.append(2)
      return

    dasima1.run_subscribers()
    dasima2.run_subscribers()

    for _ in range(number):
      publisher.exchange_type_one.send_message({}, "one")

    # Wait for received message to be processed
    time.sleep(number * 0.01)

    counter = Counter(count_list)

    assert counter[1] == number // 2
    assert counter[2] == number // 2

    dasima1.stop_subscribers()
    dasima2.stop_subscribers()

  @pytest.mark.parametrize("number", [2, 10, 100])
  def test_exchange_type_all_recive(self, dasima1, dasima2, publisher, number, count_list):

    @dasima1.exchange_type_all.subscribe("all")
    def test_subscribe_function_1():
      count_list.append(1)
      return

    @dasima2.exchange_type_all.subscribe("all")
    def test_subscribe_function_2():
      count_list.append(2)
      return

    dasima1.run_subscribers()
    dasima2.run_subscribers()

    for _ in range(number):
      publisher.exchange_type_all.send_message({}, "all")

    # Wait for received message to be processed
    time.sleep(number * 0.01)

    counter = Counter(count_list)

    assert counter[1] == number
    assert counter[2] == number

    dasima1.stop_subscribers()
    dasima2.stop_subscribers()
