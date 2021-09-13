import timeit
from flask import Flask

import sys, os

sys.path.append(os.getcwd())
from dasima import DasimaMQ

default_cdmdir = f"{os.getcwd()}/example/main/default.cfg"

dasimamq = DasimaMQ()

def create_app(config_filename=default_cdmdir):
  app = Flask(__name__)
  app.config.from_pyfile(config_filename)

  dasimamq.init_app(app=app)

  def test_time():
    dasimamq.clue.send_message({}, "info")
    dasimamq.clue.send_message({"x": 3, "y": 3}, "add")
    dasimamq.clue.send_message({"x": 3, "y": 3}, "mul")
    dasimamq.login.send_message({"x": 3, "y": 3}, "div")
    dasimamq.login.send_message({"x": 3, "y": 3}, "sub")

  @app.route("/")
  def send_message():
    result = timeit.timeit(test_time, number=10)
    print(result)
    return {"data": "Send message successful"}

  with app.app_context():

    # subscribe funtions import
    pass
  
  return app

if __name__ == "__main__":
  app = create_app()
  app.run(debug=False, host="0.0.0.0", port=sys.argv[1])
