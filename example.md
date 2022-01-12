Producer: 메세지를 보내는 Application

Publish: Producer가 메세지를 보냄

Queue: 메세지를 저장하는 버퍼

Consumer : 메세지를 받기 위해 대기 하는 프로그램



Exchange

Producer가 전달한 메시지를 Queue에 전달하는 역할





Connectoin: 메세지 브로커에 대한 실제 TCP 연결



Channel

- 내부의 가상 연결(AMQP 연결)

- TCP연결을 과부하 시키지 않오 애플리케이션 내에서 원하는 만큼 연결 사용

- 스레드가 여러개인 경우 스레드 Channel 마다 다른 것을 사용 하는게 좋음

  



