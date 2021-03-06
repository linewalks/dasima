# DASIMA

#### Description

Dasima is a library that helps you send and receive messages in Flask project. It is a simple wrapper around Kombu and support with the publisher/subscriber pattern of your Flask project.




## Getting Started

#### Built With

* Python >=  3.6



#### Prerequisites

- Message Queue 

  > ex) Redis, RabbitMQ, ActiveMQ, ZeroMQ, Kafka...



#### Installation

##### Installing

```shell
$ pip install dasima
```



##### setting parameters

```python
DASIMA_CONNECTION_HOST = "localhost" # your Message Queue host ex) redis://0.0.0.0, amqp://id:password@0.0.0.0:port
DASIMA_ACCEPT_TYPE = "json" # sending data type ex) json, pickle ...
DASIMA_EXCHANGE_SETTING = [("test_exchange", "one"),] 
# DASIMA_EXCHANGE_SETTING is list of tuples [(exchange name, type)]
# There are two types: 'all' and 'one'.
```



## Usage

#### Subscriber Simple example

```python
from dasima import Dasima
from flask import Flask


app = Flask(__name__)

dasimamq = Dasima()
dasimamq.init_app(app) # Alternatively, auto init_app can be used after putting the flask app into Dasima like Dasima(app).


# Be able to subscribe target functions using the function 'subscribe' 
# The queue named by subscribed function name will be made, and binding it with routing key
# dasimamq.{exchange}.subscribe(routing_key) - "Route key to bind"
@dasimamq.test_exchange.subscribe(routing_key="test_routing_key")
# @dasimamq.test_exchange.subscribe - if routing key not defined, routing key is defined as function name
def test_function(x, y):
    print(x + y)
    return x + y


if __name__ == "__main__":
 # Call the function 'run_subscribers' to create queues in which consumers process the messages.
    dasimamq.run_subscribers()
    app.run(port=5050)
```



#### Publisher Simple example

```python
from flask import Flask
from dasima import Dasima


app = Flask(__name__)


dasimamq = Dasima()
dasimamq.init_app(app) # Alternatively, auto init_app is possible by putting the flask app directly into Dasima(app).


@app.route("/")
def send_message():
    # dasimamq.{exchange}.subscribe("Route key to bind")
    dasimamq.test_exchange.send_message({"x": 1, "y": 2}, "test_routing_key")
    return {"data": "send message successful"}


if __name__ == "__main__":
    app.run(port=5000)
```



## Links

- [Kombu github](https://github.com/celery/kombu)
- [Redis](https://redis.io/)
- [RabbitMQ](https://www.rabbitmq.com/)



## Contact

**JISU JEONG** - js.jeong@linewalks.com

