# Importing the socket module 
import socket

# Defining a class for the game board
class BoardClass():
    # Initializing class variables
    username = ''
    prevTurnUser = 0
    NumGamesPlayed = 0
    NumWins = 0
    NumTies = 0
    NumLosses = 0

    otherUser = ''
    aSocket = 0
    inclassturn = 0
    marker = 0
    oppMarker = 0

    # Constructor method
    def __init__(self, socket, user_type):
        self.aSocket = socket
        self.inclassturn = user_type
        
        # Setting up user details and connection based on user type
        if user_type == 1:
            self.username = input('Enter your username: ')
            self.aSocket.send(self.username.encode())
            self.otherUser = self.aSocket.recv(256).decode()
            self.marker = 'X'
            self.oppMarker = 'O'
            print(f"Game will start once {self.otherUser} sends their username.")
        else:
            self.username = 'Player 2'
            self.otherUser = self.aSocket.recv(256).decode()
            self.aSocket.send(self.username.encode())
            self.marker = 'O'
            self.oppMarker = 'X'

        # Creating a 3x3 empty game board
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.printBoard()
        self.play()

    # Printing the game board
    def printBoard(self):
        for row in self.board:
            print(' | '.join(row))
            print('-' * 9)

    # Main game loop
    def play(self):
        while True:
            if self.inclassturn == 1:
                self.makeMove()
                self.aSocket.send(self.serializeMove().encode())
            else:
                opp_move = self.aSocket.recv(1024).decode()
                self.updateBoard(opp_move)
                self.printBoard()
                if self.isWinner(self.oppMarker):
                    print(f"{self.otherUser} wins!")
                    self.NumLosses += 1
                    self.resetGameBoard()
                elif self.boardIsFull():
                    print("It's a tie!")
                    self.NumTies += 1
                    self.resetGameBoard()
                else:
                    self.makeMove()
                    self.aSocket.send(self.serializeMove().encode())
                    self.printBoard()
                    if self.isWinner(self.marker):
                        print(f"{self.username} wins!")
                        self.NumWins += 1
                        self.resetGameBoard()
                    elif self.boardIsFull():
                        print("It's a tie!")
                        self.NumTies += 1
                        self.resetGameBoard()

    # Allowing the current player to make a move
    def makeMove(self):
        row = int(input("Enter row (0-2): "))
        col = int(input("Enter column (0-2): "))
        if self.board[row][col] == ' ':
            self.board[row][col] = self.marker
        else:
            print("Invalid move. Try again.")
            self.makeMove()

    # Updating the board based on the opponent's move
    def updateBoard(self, move):
        row, col = self.deserializeMove(move)
        self.board[row][col] = self.oppMarker

    # Checking if the specified player has won
    def isWinner(self, player_marker):
        # Checking rows, columns, and diagonals for a win
        for i in range(3):
            if all(self.board[i][j] == player_marker for j in range(3)) or \
               all(self.board[j][i] == player_marker for j in range(3)):
                return True
        return all(self.board[i][i] == player_marker for i in range(3)) or \
               all(self.board[i][2 - i] == player_marker for i in range(3))

    # Checking if the game board is full
    def boardIsFull(self):
        return all(cell != ' ' for row in self.board for cell in row)

    # Resetting the game board and display player statistics
    def resetGameBoard(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.printStats()

    # Printing player statistics
    def printStats(self):
        print(f"Stats for {self.username}:")
        print(f"Total Games Played: {self.NumGamesPlayed}")
        print(f"Wins: {self.NumWins}")
        print(f"Ties: {self.NumTies}")
        print(f"Losses: {self.NumLosses}")
        exit()

    # Serializing the move into a string
    def serializeMove(self):
        return f"{self.prevTurnUser}{self.row}{self.col}"

    # Deserializing a move from a string
    def deserializeMove(self, move):
        return int(move[1]), int(move[2])

# Entry point of the program
if __name__ == "__main__":
    # Getting server address and port from user input
    serverAddress = input('Enter the IP: ')
    serverPort = int(input('Enter the port: '))
    
    # Creating a socket and connect to the server
    aSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    aSocket.connect((serverAddress, serverPort))
    
    # Getting user type (1 or 2) from user input
    user_type = int(input("Enter your user type (1 for Player 1, 2 for Player 2): "))
    
    # Creating an instance of the BoardClass and start the game
    gameboard = BoardClass(aSocket, user_type)
