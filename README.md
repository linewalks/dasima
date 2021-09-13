# CLUE-MQ


### Quick start

#### subscriber

```python
from dasima import DasimaMQ


dasimamq = DasimaMQ(
    host="localhost", # your Message Queue host ex) redis://0.0.0.0, amqp://id:password@0.0.0.0:port
    exchange_list=[("clue", "topic")], 
    accept_type="json" # 전송 받을 data type
)


# subscribe을 통해서 함수의 구독이 가능함
# 구독한 함수 이름의 큐가 만들어 지며 설정한 routing key로 바인딩
#dasimamq.{exchange}.subscribe("바인딩 시킬 라우팅 키")
@dasimamq.clue.subscribe("test_routing_key")
def test_function(x, y):
  return x + y


if __name__ == "__main__":
  # run_subscribers 함수를 통해서
  # 지금까지 설정된 큐와 큐의 메세지를 소비하는 Comsumer를 생성 해줌
  dasimamq.run_subscribers()

```


#### Publisher
```python
from dasima import DasimaMQ


dasimamq = DasimaMQ(
    host="localhost", # your Message Queue host ex) redis://0.0.0.0, amqp://id:password@0.0.0.0:port
    exchange_list=[("clue", "topic")], 
    accept_type="json" # 전송 받을 data type
)


#dasimamq.{exchange}.send_message(전송 데이터 dict type, "요청을 보낼 라우팅키")
dasimamq.clue.send_message({"x": 1, "y": 2}, "test_routing_key")
```

