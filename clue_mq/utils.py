from functools import update_wrapper


def setup(func):
  def wrapper(*args, **kwargs):
    return func(*args, **kwargs)
  return update_wrapper(wrapper, func)