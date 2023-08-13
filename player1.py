import socket

from gameboard import BoardClass

def startConnection():
    serverAddress = input('Enter the IP: ')
    serverPort = int(input('Enter the port: '))
    try:
        aSocket.connect((serverAddress, serverPort))
    except ConnectionRefusedError:
        retryConnection = input('Do you want to try connecting again? (y/n): ')
        if retryConnection == 'y':
            startConnection()
        elif retryConnection == 'n':
            quit()
        else:
            print("Invalid option. Terminating.")
            quit()

if __name__ == '__main__':
    aSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    startConnection()
    print('Connected!')
    aSocket.send(b'Connected!')
    user_type = 1
    gameboard = BoardClass(aSocket, user_type)
