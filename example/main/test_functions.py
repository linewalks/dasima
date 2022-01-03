from flask import current_app as app
from main import dasimamq


@dasimamq.clue.subscribe("info")
def setting_info():
  print("Dasima setting parameters")
  print("DASIMA_CONNECTION_HOST: ", app.config["DASIMA_CONNECTION_HOST"])
  print("DASIMA_ACCEPT_TYPE: ", app.config["DASIMA_ACCEPT_TYPE"])
  print("DASIMA_EXCHANGE_SETTING: ", app.config["DASIMA_EXCHANGE_SETTING"])

# 설정된 key(add)로 바인딩
@dasimamq.clue.subscribe("add")
def add(x, y):
  print("ADD", x, y)
  return x + y

# 설정된 key 없을 시 함수 이름 mul로 바인딩
@dasimamq.clue.subscribe()
def mul(x, y):
  print("MUL", x, y)
  return x * y

# () 없을 때도 위와 같은 함수 이름 div로 바인딩
@dasimamq.login.subscribe
def div(x, y):
  print("DIV", x, y)
  return x // y

# 설정된 key(test)로 바인딩
@dasimamq.login.subscribe("test")
def sub(x, y):
  print("SUB", x, y)
  return x - y
