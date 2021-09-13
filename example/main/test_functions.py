from flask import current_app as app
from main import dasimamq


@dasimamq.clue.subscribe("info")
def setting_info():
  print("Dasima setting parameters")
  print("MESSAGE_QUEUE_HOST: ", app.config["MESSAGE_QUEUE_HOST"])
  print("MESSAGE_QUEUE_ACCEPT_TYPE: ", app.config["MESSAGE_QUEUE_ACCEPT_TYPE"])
  print("MESSAGE_QUEUE_EXCHANGE_SETTING: ", app.config["MESSAGE_QUEUE_EXCHANGE_SETTING"])


@dasimamq.clue.subscribe("add")
def add(x, y):
  print("ADD", x, y)
  return x + y


@dasimamq.clue.subscribe("mul")
def mul(x, y):
  print("MUL", x, y)
  return x * y


@dasimamq.login.subscribe("div")
def div(x, y):
  print("DIV", x, y)
  return x // y


@dasimamq.login.subscribe("sub")
def sub(x, y):
  print("SUB", x, y)
  return x - y
