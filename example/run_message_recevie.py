import sys
from main import create_app, dasimamq

if __name__ == "__main__":
  app = create_app()
  dasimamq.run_subscribers()
  app.run(debug=False, host="0.0.0.0", port=sys.argv[1])
