import pytest
from pytest_mock import mocker


class TestMQ:
  def test_setting(self):



  def test_add_queue(self, cluemq):
    def add(x, y):
      return x + y


    def mul(x, y):
      return x * y


    def div(x, y):
      return x // y

    cluemq.add_queue("clue.add", add, "test")
    cluemq.add_queue("clue.mul", mul, "test")
    cluemq.add_queue("clue.div", div, "test")

  def test_send_message(self, cluemq):
    cluemq.send_message({"x": 3, "y": 3}, routing_key="clue.add", serializer="json")
    cluemq.send_message({"x": 3, "y": 3}, routing_key="clue.mul", serializer="json")
    cluemq.send_message({"x": 3, "y": 3}, routing_key="clue.div", serializer="json")
