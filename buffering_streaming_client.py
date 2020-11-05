import socket

HEADER_SIZE = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create client socket
s.connect((socket.gethostname(), 1234))

while True:
    full_msg = ''
    new_msg = True
    while True:
        
        msg = s.recv(16) #Current buffer is 16
        if new_msg:
            print(f"New message lenth: {msg[:HEADER_SIZE]}")
            msglen = int(msg[:HEADER_SIZE])
            new_msg = False

        full_msg += msg.decode("utf-8")
        if len(full_msg) - HEADER_SIZE == msglen:
            print("full msg revcd")
            print(full_msg[HEADER_SIZE:])
            recvd = "Message received from client"
            s.send(bytes(recvd, "utf-8"))
            new_msg = True
            full_msg = ''
        
        
        


    print(full_msg)
