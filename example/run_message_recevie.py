import sys
from main import create_app, cluemq

if __name__ == "__main__":
  app = create_app()
  cluemq.run_subscribers()
  app.run(debug=False, host="0.0.0.0", port=sys.argv[1])
