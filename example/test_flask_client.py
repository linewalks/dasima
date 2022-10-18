import random

from flask import Flask
from dasima import Dasima


dasimamq = Dasima()


def create_app():
  app = Flask(__name__)
  app.config.update({
      "DASIMA_CONNECTION_HOST": "pyamqp://localhost:5672",
      "DASIMA_ACCEPT_TYPE": "json",
      "DASIMA_EXCHANGE_SETTING": [("clue", "one"), ("login", "all")]
  })

  dasimamq.init_app(app)  # Alternatively, auto init_app is possible by putting the flask app directly into Dasima(app).
  with app.app_context():
    def test_function():
      dasimamq.clue.send_message({"x": 3, "y": 3}, "add")
      dasimamq.login.send_message({"x": 3, "y": 3}, "mul")

      input = random.randint(0, 10000)
      output = dasimamq.clue.send_message_and_recevie_result({"x": input}, "linear")
      print(input, output)
      assert input == output

    @app.route("/")
    def test_home():
      for _ in range(10):
        test_function()
      return {"data": "Send message successful"}

  return app


if __name__ == "__main__":
  app = create_app()
  app.run(port=5001)
