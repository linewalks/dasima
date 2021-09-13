from flask import Flask

import sys, os

sys.path.append(os.getcwd())
from clue_mq import ClueMQ

default_cdmdir = f"{os.getcwd()}/example/main/default.cfg"

cluemq = ClueMQ()

def create_app(config_filename=default_cdmdir):
  app = Flask(__name__)
  app.config.from_pyfile(config_filename)

  cluemq.init_app(app=app)

  with app.app_context():

    # subscribe funtions import
    from main.test_functions import (
        setting_info,
        add,
        mul,
        div,
        sub
    )
  
  return app