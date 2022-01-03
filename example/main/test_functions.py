from flask import current_app as app
from main import dasimamq


@dasimamq.clue.subscribe("info")
def setting_info():
  print("Dasima setting parameters")
  print("DASIMA_CONNECTION_HOST: ", app.config["DASIMA_CONNECTION_HOST"])
  print("DASIMA_ACCEPT_TYPE: ", app.config["DASIMA_ACCEPT_TYPE"])
  print("DASIMA_EXCHANGE_SETTING: ", app.config["DASIMA_EXCHANGE_SETTING"])


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
