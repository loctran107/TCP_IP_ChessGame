#Create a server chess game
import socket

HEADER_SIZE = 10
#Initialize the socket, make it global
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.131", 65432))


#Variables global to the field
width = height = 8
SUCCESS = 0
FAILURE = 1

def SetupChessBoard():
    global chessBoard
    global chessMap

    chessMap = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4, 'f' : 5,
                'g' : 6, 'h' : 7}
    #Defining 2-D array of 8x8
    chessBoard = [[0 for x in range(width)] for y in range(height)]
    
    #Setting up the chessboard
    chessBoard[0][0] = 'R'
    chessBoard[0][1] = 'N'
    chessBoard[0][2] = 'B'
    chessBoard[0][3] = 'Q'
    chessBoard[0][4] = 'K'
    chessBoard[0][5] = 'B'
    chessBoard[0][6] = 'N'
    chessBoard[0][7] = 'R'

    for i in range(8):
        chessBoard[1][i] = 'P'
        chessBoard[6][i] = 'p'
        
    for i in range(8):
        chessBoard[2][i] = '.'
        chessBoard[3][i] = '.'
        chessBoard[4][i] = '.'
        chessBoard[5][i] = '.'

    chessBoard[7][0] = 'r'
    chessBoard[7][1] = 'n'
    chessBoard[7][2] = 'b'
    chessBoard[7][3] = 'q'
    chessBoard[7][4] = 'k'
    chessBoard[7][5] = 'b'
    chessBoard[7][6] = 'n'
    chessBoard[7][7] = 'r'
    
def PrintChessBoard():
    print()
    for i in range(width):
        print(height - i, end= "  ")
        for j in range(height):
            print(chessBoard[i][j], end= " ")
        print()
    print()
    print("   a b c d e f g h")
    print()

def PrintRule():
    print("****************RULE****************")
    print("1) Player 1 with lowercase letter moves first")
    print("2) Each player takes turn to move a piece")
    print("3) Each player must enter valid move")
    print("4) Enter the move when prompted a piece name followed by a character followed by a digit")
    print("   Example: a4e5 or e5a4 are the valid move")
    print("4) If any player puts a move in a position where there is not")
    print("   a piece, the program would exit.")
    print("5) If any player decides to quit, or rage quit the game, neither")
    print("   would win. To quit, please enter 'quit' or 'QUIT' when prompted")


def CheckNotValid(player):
    if len(player) != 4:
        return True
    if (player[0].lower() in chessMap.keys()) and\
       ((int(player[1]) - 1) in chessMap.values()) and\
       (player[2].lower() in chessMap.keys()) and\
       ((int(player[3]) - 1) in chessMap.values()):
        return False
    return True

def UpdateChessBoard(player):
    if CheckNotValid(player):
        return FAILURE
    p1 = chessBoard[8 - int(player[1])][chessMap.get(player[0])] #from
    p2 = chessBoard[8 - int(player[3])][chessMap.get(player[2])] #to

    if p1 == '.':
        return FAILURE #Failure: to exit the program

    #Handle capture piece
    if p2 != '.': #destination different from blank

        #remove the piece at p2
        p2 = '.' 

    #Swap
    temp = p1
    p1 = p2
    p2 = temp

    chessBoard[8 - int(player[1])][chessMap.get(player[0])] = p1
    chessBoard[8 - int(player[3])][chessMap.get(player[2])] = p2

    return SUCCESS
    
def Server():

    #Receive information from server
    server = ''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            msglen = int(msg[:HEADER_SIZE])
            new_msg = False

        server += msg.decode("utf-8")
        if len(server) - HEADER_SIZE == msglen: #Received full messgage from server
            new_msg = True
            break

    #Extract the exact string
    server = server[HEADER_SIZE:]
    
    #Check for rage quit
    if server.lower() == "quit": #rage quit
        print("Since one the players quit. The match is draw.")
        print("Game over. Thank you for playing")
        return FAILURE
   
    #Update the chessBoard accordingly
    if UpdateChessBoard(server):
        print("Error: Update unsucessful")
        print("Exit the game")
        return FAILURE

    PrintChessBoard()
    return SUCCESS

def Client():
    __status__ = SUCCESS

    #Prompt for client input
    client = str(input("Client's turn: "))
    #Handle client string
    if client.lower() == "quit": #rage quit
        print("Since one the players quit. The match is draw.")
        print("Game over. Thank you for playing")
        __status__ = FAILURE
    
    if __status__ == SUCCESS:
        while CheckNotValid(client):
            print("Error: Invalid move. Server player! please enter the move again.")
            client = str(input("Server's turn: "))

        #Update the chessBoard accordingly
        if UpdateChessBoard(client):
            print("Error: Update unsucessful")
            print("Exit the game")
            client = "fails"
            __status__ = FAILURE

    
    client = f'{len(client):<{HEADER_SIZE}}' + client
    #Send string client to server
    s.send(bytes(client, "utf-8"))

    if __status__ == SUCCESS:
        PrintChessBoard()
    return __status__
    
def main():
    
    print("Welcome to the chess game")
    #Check for valid response
    toPlay = str(input("Do you want to play the game(Y/N): "))
    while ("Y" not in toPlay) and ('N' not in toPlay):
        print("Error. Invalid input. Please enter again.")
        toPlay = str(input("Do you want to play the game(Y/N): "))

    if toPlay == "Y":
        
        SetupChessBoard()

        PrintRule()
        PrintChessBoard()

        while True:
            server_status = Server()
            if server_status == FAILURE:
                break
            client_status = Client()
            if client_status == FAILURE:
                break
main()
