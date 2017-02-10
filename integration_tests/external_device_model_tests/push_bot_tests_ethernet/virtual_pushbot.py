from socket import socket
import traceback
sock = socket()
sock.bind(("0.0.0.0", 56000))
sock.listen(1)

while True:
    print "Waiting for connection"
    connection, client = sock.accept()
    print "Client Connected from {}".format(client)

    is_data = True
    while is_data:
        data = None
        try:
            data = connection.recv(200)

            if not data:
                is_data = False
            else:
                print "RECV: {}".format(data)
        except:
            traceback.print_exc()
            is_data = False
