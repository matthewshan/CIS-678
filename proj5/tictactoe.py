# [ col 1: [row top, mid, bottom], col 2, col 3 ]
# Thus, coordinates must be list[col][row], like the board
board = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
currentPlayer = 0

def ticTacGo():
    pass

def returnValidSpaces():
    global board
    validLocations = []
    # Rows and cols, 0, 1, 2
    for col in range(3):
        for row in range(3):
            if (board[col][row] == -1):
                validLocations.append([row, col])
    return validLocations

def isValidLocation(coordinates):
    global board
    if (board[coordinates[0]][coordinates[1]] == -1):
        return True
    return False

def doTurn(coordinates):
    global currentPlayer, board
    if (isValidLocation(coordinates)):
        board[coordinates[0]][coordinates[1]] = currentPlayer
        currentPlayer = (currentPlayer + 1) % 2
    else:
        print("Invalid location")

def hasWon(playerID):
    global board
    # check middle cases
    if (board[1][1] == playerID):
        # horizontal middle
        if (board[1][0] == playerID and board[1][2] == playerID):
            return True
        # vertical middle
        elif (board[0][1] == playerID and board[2][1] == playerID):
            return True
        # diagonal w/ top left
        elif (board[0][0] == playerID and board[2][2] == playerID):
            return True
        # diagonal w/ top right
        elif (board[2][0] == playerID and board [0][2] == playerID):
            return True
    # check top horiz and left vert
    elif (board[0][0] == playerID):
        # top horiz
        if (board[1][0] == playerID and board[2][0] == playerID):
            return True
        # left vert
        elif (board[0][1] == playerID and board[0][2] == playerID):
            return True
    # check bottom horiz and right vert
    elif (board[2][2] == playerID):
        # bottom horiz
        if (board[1][2] == playerID and board[2][2] == playerID):
            return True
        # right vert
        elif (board[2][1] == playerID and board[2][2] == playerID):
            return True
    return False

def checkTie():
    global board
    foundEmptySpace = False
    for col in range(3):
        for row in range(3):
            if (board[col][row] == -1):
                foundEmptySpace = True
    if (not foundEmptySpace and not hasWon(0) and not hasWon(1)):
        return True
    return False