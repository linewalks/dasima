# DASIMA


### Quick start

### setting parameters
```python
DASIMA_CONNECTION_HOST = "localhost" # your Message Queue host ex) redis://0.0.0.0, amqp://id:password@0.0.0.0:port
DASIMA_ACCEPT_TYPE = "json" # sending data type json, pickle ...
DASIMA_EXCHANGE_SETTING = [("dasima_test", "topic"),]
```

#### Subscriber

```python

from flask import Flask
from dasima import Dasima

app = Flask(__name__)

dasimamq = Dasima()
dasimamq.init_app(app) # Alternatively, auto init_app can be used after putting the flask app into Dasima like Dasima(app).

# Be able to subscribe target functions using the function 'subscribe' 
# The queue named by subscribed function name will be made, and binding it with routing key
# dasimamq.{exchange}.subscribe("Route key to bind")
@dasimamq.dasima_test.subscribe("test_routing_key")
def test_function(x, y):
  print(x + y)
  return x + y


if __name__ == "__main__":
  # Create queues that were established
  # and consumers that process the messages in queues
  # as implement the function 'run_subscribers'
  dasimamq.run_subscribers()
  app.run(port=5050)
```



#### Publisher

```python
from flask import Flask
from dasima import Dasima

app = Flask(__name__)

dasimamq = Dasima()
dasimamq.init_app(app) # Alternatively, auto init_app is possible by putting the flask app directly into Dasima(app).

@app.route("/")
def send_message():
  # dasimamq.{exchange}.subscribe("Route key to bind")
  dasimamq.dasima_test.send_message({"x": 1, "y": 2}, "test_routing_key")
  return {"data": "send message successful"}

if __name__ == "__main__":
  app.run(port=5000)
```