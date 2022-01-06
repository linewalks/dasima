import time
import pytest
import random


class TestMQ:
  @pytest.fixture(scope="class")
  def test_cnt(self):
    value = {
        "one_cnt_1": 0,
        "one_cnt_2": 0,
        "all_cnt_1": 0,
        "all_cnt_2": 0
    }
    yield value

  def test_subscribe(self, subscriber_1, subscriber_2, test_cnt):
    @subscriber_1.test_type_one.subscribe("one")
    def test_one_func1():
      test_cnt["one_cnt_1"] += 1
      return

    @subscriber_2.test_type_one.subscribe("one")
    def test_one_func2():
      test_cnt["one_cnt_2"] += 1
      return

    @subscriber_1.test_type_all.subscribe("all")
    def test_all_func1():
      test_cnt["all_cnt_1"] += 1
      return

    @subscriber_2.test_type_all.subscribe("all")
    def test_all_func2():
      test_cnt["all_cnt_2"] += 1
      return

    subscriber_1.run_subscribers()
    subscriber_2.run_subscribers()

  def test_message_send_and_recevie(self, publisher, test_cnt):
    number = random.randint(1, 100)
    for i in range(number):
      publisher.test_type_one.send_message({}, "one")

    # Wait for received message to be processed
    time.sleep(number * 0.01)
    print(number)
    print(test_cnt["one_cnt_1"])
    print(test_cnt["one_cnt_2"])
