import sys, os
sys.path.append(os.getcwd())
from clue_mq import ClueMQ
from flask import Flask


app = Flask(__name__)
print(type(app))
app.config.setdefault(
    "MESSAGE_QUEUE_EXCHANGE_SETTING",
    [("clue", "topic"), ("login", "topic")]
)
cluemq = ClueMQ()

if __name__ == "__main__":
  cluemq.init_app(app=app)


  @cluemq.clue.subscribe("add")
  def add(x, y):
    print("ADD", x, y)
    return x + y


  @cluemq.clue.subscribe("mul")
  def mul(x, y):
    print("MUL", x, y)
    return x * y


  @cluemq.login.subscribe("div")
  def div(x, y):
    print("DIV", x, y)
    return x // y


  @cluemq.login.subscribe("sub")
  def sub(x, y):
    print("SUB", x, y)
    return x - y

  cluemq.run_subscribers()
  app.run(debug=False, host="0.0.0.0", port=sys.argv[1])
