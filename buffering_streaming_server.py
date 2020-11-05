import socket
import time

#Use fixed length header to send client information of buffer 
#before streaming
HEADER_SIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    clientsocket, address = s.accept() #establish connection with the client
    print(f"Connection from {address} has been established")

    msg = "Welcome to the server!"
    msg = f'{len(msg):<{HEADER_SIZE}}' + msg #Adding header which contains buffer length before message
    clientsocket.send(bytes(msg, "utf-8"))
    
    ret = clientsocket.recv(100)
    print(ret)
    
    
    '''
    time.sleep(3)
    
    msg2 = "Gotcha catch them all"
    msg2 = f'{len(msg2):<{HEADER_SIZE}}' + msg2
    clientsocket.send(bytes(msg2, "utf-8"))
    '''
    #NOTE: without closing the clientsocket, we'll be able to send 
    #      more data to the client


