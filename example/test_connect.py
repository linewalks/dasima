from kombu import Connection

rabbitmq_url = "localhost"

conn = Connection(rabbitmq_url)
print("-----declare connection-----")
print(conn)
print(f"connection : {conn.connected}\n")


connection = conn.connect()
print("-----AMQP connection-----")
print(connection)
print(f"connection : {conn.connected}\n")

conn.close()
print("-----AMQP close-----")
print(connection)
print(f"connection : {conn.connected}\n")


# close and release same def
# why does kombu declare the same def ?
print(f"def close and def release same checking {conn.close == conn.release}")

print("-----delete connection resource-----\n")
del connection
del conn


print("-----declare connection-----")
with Connection(rabbitmq_url) as conn:
  print(conn)
  print(f"connection : {conn.connected}\n")
  print("-----AMQP connection-----")

  with conn.connect() as connection:
    print(connection)
    print(f"connection : {conn.connected}\n")

  print("-----AMQP auto close-----")

print(connection)
print(f"connection : {conn.connected}")
