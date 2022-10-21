from dasima import Dasima
from flask import Flask


dasimamq = Dasima()


def create_app():
  app = Flask(__name__)
  app.config.update({
      "DASIMA_CONNECTION_HOST": "pyamqp://localhost:5672",
      "DASIMA_ACCEPT_TYPE": "json",
      "DASIMA_EXCHANGE_SETTING": [("clue", "one"), ("login", "all")]
  })

  dasimamq.init_app(app)  # Alternatively, auto init_app can be used after putting the flask app into Dasima like Dasima(app).

  @dasimamq.after_subscribe_task
  def after_work(data, message, result):
    print(f"exchange {message.delivery_info['exchange']} {message.delivery_info['routing_key']} 요청")
    print(f"{data} 전송, 처리 결과 {result}")

  with app.app_context():

    @dasimamq.clue.subscribe("add")
    def add_funtion(x, y):
      return x + y

    @dasimamq.login.subscribe("mul")
    def mul_funtion(x, y):
      return x * y

    @dasimamq.clue.subscribe("linear")
    def linear_function(x):
      y = x
      return y

  return app


if __name__ == "__main__":
 # Call the function 'run_subscribers' to create queues in which consumers process the messages.
  app = create_app()
  dasimamq.run_subscribers()
  app.run(port=5000)
