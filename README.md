# CLUE-MQ


### Quick start

### setting parameters
```python
MESSAGE_QUEUE_HOST = "localhost" # your Message Queue host ex) redis://0.0.0.0, amqp://id:password@0.0.0.0:port
MESSAGE_QUEUE_ACCEPT_TYPE = "json" # sending data type json, pikle ...
MESSAGE_QUEUE_EXCHANGE_SETTING = [("dasima_test", "topic"),]
```

#### Subscriber

```python

from flask import Flask
from dasima import DasimaMQ

app = Flask(__name__)

dasimamq = DasimaMQ()
dasimamq.init_app(app) # 또는 DasimaMQ(app) 바로 flask app을 넣어 주어서 auto init_app 가능

# subscribe을 통해서 함수의 구독이 가능함
# 구독한 함수 이름의 큐가 만들어 지며 설정한 routing key로 바인딩
#dasimamq.{exchange}.subscribe("바인딩 시킬 라우팅 키")
@dasimamq.dasima_test.subscribe("test_routing_key")
def test_function(x, y):
  print(x + y)
  return x + y


if __name__ == "__main__":
  # run_subscribers 함수를 통해서
  # 지금까지 설정된 큐와 큐의 메세지를 소비하는 Comsumer를 생성 해줌
  dasimamq.run_subscribers()
  app.run(port=5050)
```



#### Publisher

```python
from flask import Flask
from dasima import DasimaMQ

app = Flask(__name__)

dasimamq = DasimaMQ()
dasimamq.init_app(app) # 또는 DasimaMQ(app) 바로 flask app을 넣어 주어서 auto init_app 가능

@app.route("/")
def send_message():
  #dasimamq.{exchange}.send_message(전송 데이터 dict type, "요청을 보낼 라우팅키")
  dasimamq.dasima_test.send_message({"x": 1, "y": 2}, "test_routing_key")
  return {"data": "send message successful"}

if __name__ == "__main__":
  app.run(port=5000)
```