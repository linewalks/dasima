def add(x,y):
  print(x+y)
  return x+y

def mul(x,y):
  print(x*y)
  return x*y

def print_hello():
  print("hello")
  return "hello"

func_list = [
    ("add", add),
    ("mul", mul),
    ("print", print_hello)
]

def make_binding_func(func_list):
  def func(data, key):
    func_dict = dict(func_list)
    if func_dict.get(key):
      return func_dict[key](**data)
    return "error"
  return func

custom = make_binding_func(func_list)

custom({"x":1, "y":4}, "add")
custom({"x":1, "y":4}, "mul")
custom({}, "print")

    