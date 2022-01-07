import pytest
import time
import random


class TestMQ:
  @pytest.fixture(scope="class")
  def test_cnt(self):
    value = {
        "one_cnt_1": 0,
        "one_cnt_2": 0,
        "all_cnt": 0
    }
    yield value

  def test_subscribe(self, subscriber_1, subscriber_2, publisher, test_cnt):
    @subscriber_1.test_type_one.subscribe("one")
    def test_one_func1():
      test_cnt["one_cnt_1"] += 1
      return

    @subscriber_2.test_type_one.subscribe("one")
    def test_one_func2():
      test_cnt["one_cnt_2"] += 1
      return

    # when there is not routing key, routing key is set automatically function name
    @subscriber_1.test_type_all.subscribe
    @subscriber_2.test_type_all.subscribe
    def test_all_func():
      test_cnt["all_cnt"] += 1
      return

    subscriber_1.run_subscribers()
    subscriber_2.run_subscribers()

    number = random.randint(1, 100) * 2
    for i in range(number):
      publisher.test_type_one.send_message({}, "one")
      publisher.test_type_all.send_message({}, "test_all_func")

    # Wait for received message to be processed
    time.sleep(number * 0.01)

    assert test_cnt["one_cnt_1"] == number // 2
    assert test_cnt["one_cnt_2"] == number // 2
    assert test_cnt["all_cnt"] == number * 2
