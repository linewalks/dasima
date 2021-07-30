from kombu import Connection


class ClueMQ:
  def __init__(self, host):
    self.conn = Connection(host)

  def connect(self):
    self.conn.connect()

  def close(self):
    self.conn.close()
