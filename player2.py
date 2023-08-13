import socket

from gameboard import BoardClass

def startServer():
    serverAddress = '127.0.0.1'
    port = 8000
    aSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    aSocket.bind((serverAddress, port))
    aSocket.listen(1)
    bSocket, bAddress = aSocket.accept()
    clientmsg = bSocket.recv(1024).decode('ascii')
    print(clientmsg)
    user_type = 2
    gameboard = BoardClass(bSocket, user_type)

if __name__ == "__main__":
    startServer()
