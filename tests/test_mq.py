import pytest
import time
import random

from collections import Counter
from dasima import Dasima


class TestSetup:
  def test_init_app(self, app):
    dasmia1 = Dasima(app)
    dasmia2 = Dasima()
    dasmia2.init_app(app)
    assert dasmia1.app == dasmia2.app

  def test_create_exchange(self, exchange_setting_list, app):
    dasima = Dasima(app)
    for exchange_name, exchange_type in exchange_setting_list:
      exchange = getattr(dasima, exchange_name)
      assert exchange.exchange_type == exchange_type
      assert exchange.exchange.name == exchange_name


class TestSubscribe:
  @pytest.fixture(scope="function")
  def dasima(self, app):
    return Dasima(app)

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


class TestMessageSendReceive:
  @pytest.fixture(scope="function")
  def sub1(self, app):
    return Dasima(app)

  @pytest.fixture(scope="function")
  def sub2(self, app):
    return Dasima(app)

  @pytest.fixture(scope="function")
  def pub(self, app):
    return Dasima(app)

  @pytest.mark.parametrize("number", [2, 10, 100])
  def test_exchange_type_one_recive(self, sub1, sub2, pub, number):
    count_list = []

    @sub1.exchange_type_one.subscribe("one")
    def test_subscribe_function_1():
      count_list.append(1)
      return

    @sub2.exchange_type_one.subscribe("one")
    def test_subscribe_function_2():
      count_list.append(2)
      return

    sub1.run_subscribers()
    sub2.run_subscribers()

    for _ in range(number):
      pub.exchange_type_one.send_message({}, "one")

    # Wait for received message to be processed
    time.sleep(number * 0.01)

    counter = Counter(count_list)

    assert counter[1] == number // 2
    assert counter[2] == number // 2

    sub1.stop_subscribers()
    sub2.stop_subscribers()

  @pytest.mark.parametrize("number", [2, 10, 100])
  def test_exchange_type_all_recive(self, sub1, sub2, pub, number):
    count_list = []

    @sub1.exchange_type_all.subscribe("all")
    def test_subscribe_function_1():
      count_list.append(1)
      return

    @sub2.exchange_type_all.subscribe("all")
    def test_subscribe_function_2():
      count_list.append(2)
      return

    sub1.run_subscribers()
    sub2.run_subscribers()

    for _ in range(number):
      pub.exchange_type_all.send_message({}, "all")

    # Wait for received message to be processed
    time.sleep(number * 0.01)

    counter = Counter(count_list)

    assert counter[1] == number
    assert counter[2] == number

    sub1.stop_subscribers()
    sub2.stop_subscribers()

  def test_send_message_and_recevie_result(self, sub1, pub):

    @sub1.exchange_type_one.subscribe("linear")
    def test_linear_function(x):
      y = x
      return y

    sub1.run_subscribers()

    random_input = random.randint(0, 10000)
    output = pub.exchange_type_one.send_message_and_recevie_result(
        {"x": random_input},
        "linear"
    )
    assert random_input == output

    sub1.stop_subscribers()
