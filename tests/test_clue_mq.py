import pytest



#exchange, exchange Type parameter declare
class TestMQ:

  @pytest.fixture(scope="class")
  def setup_funtion(self):
    # Declare test exchange, test Queue
    
    yield
    
    # Delete test exchange, test Queue  
  
  def test_add_queue_func(self, cluemq):
    @cluemq.setup_queue("clue.add", "test")
    def add(x, y):
      return x + y

    @cluemq.setup_queue("clue.mul", "clue")
    def mul(x, y):
      return x * y

    def div(x, y):
      return x // y
    
    cluemq.add_queue(div, "clue.div", "test")
    # check adding Queue list
  
  def test_message_send_func(self, cluemq):
    cluemq.send_message({"x": 3, "y": 3}, routing_key="clue.add", serializer="json")
    # check sending message data assert ---check logic----
    # check matching Routing keys assert ---check logic----
  
  def test_receive_message(self, cluemq):
    pass

  def test_multi_heavy_load(self):
    pass
