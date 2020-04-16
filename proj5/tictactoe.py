import random
# [ col 1: [row top, mid, bottom], col 2, col 3 ]
# Thus, coordinates must be list[col][row], like the board
board = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
# Keys = integer version of the board, value is the q value (or whatever is needed)
stateDict = {}
currentPlayer = 0
# Not sure if needed, but our "time" for Q learning. Increments by 1 every time someone makes a move
turnNumber = 0

# This is where we will do all the stuff with Q learning and whatnot
def ticTacGo():
    global turnNumber, currentPlayer
    winCount = [0, 0]
    gameCount = 0
    totalTies = 0
    while (gameCount < 1000):
        currPlay = currentPlayer
        row = random.randint(0,2)
        col = random.randint(0,2)
        didTurn = False
        # This if isn't needed, but just so we don't get a bunch of prints
        if (isValidLocation([col, row])):
            doTurn([col, row])
            didTurn = True

        if (didTurn):
            # If the player who did a move won
            if (hasWon(currPlay)):
                winCount[currPlay] += 1
                gameCount += 1
                print ("Player " + str(currPlay) + " won game " + str(gameCount) + " after " + str(turnNumber) + " total moves.")
                print("--Total wincount--")
                print ("Player 1: " + str(winCount[0]))
                print("Player 2: " + str(winCount[1]))
                print("Total ties: " + str(totalTies) + "\n")
                resetBoard()
            elif (checkTie()):
                totalTies += 1
                gameCount += 1
                print ("Game " + str(gameCount) + " has ended in a tie after " + str(turnNumber) + " total moves.")
                print("--Total wincount--")
                print ("Player 1: " + str(winCount[0]))
                print("Player 2: " + str(winCount[1]))
                print("Total ties: " + str(totalTies) + "\n")
                resetBoard()


# Resets the board to be all empty
def resetBoard():
    global board, currentPlayer, turnNumber
    board = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
    currentPlayer = 0
    turnNumber = 0

# Translates the board from a 2D array to a 9 number long integer.
# should be col 111222333 for the format, with 111 being top to bottom of col 1
def translateBoard(boardState):
    global board
    numberString = ""
    for col in range(3):
        for row in range(3):
            numberString += board[col][row]
    return int(numberString)

# Gets the value of a specific board state, reward, etc
def getStateValue(boardState):
    global stateDict
    translatedState = translateBoard(boardState)
    try:
        return stateDict["translatedState"]
    except:
        print("Could not find board state.")
        return None

# Sets the value of a specific board state, reward, etc
def setStateValue(boardState, val):
    global stateDict
    stateDict[translateBoard(boardState)] = val

# Returns a list of all unused places on the board
def returnValidSpaces():
    global board
    validLocations = []
    # Rows and cols, 0, 1, 2
    for col in range(3):
        for row in range(3):
            if (board[col][row] == -1):
                validLocations.append([row, col])
    return validLocations

# Checks to see if the given [col, row] coordinates are valid
def isValidLocation(coordinates):
    global board
    if (board[coordinates[0]][coordinates[1]] == -1):
        return True
    return False

# Puts a piece at the given coordinates for the current player
def doTurn(coordinates):
    global currentPlayer, board, turnNumber
    if (isValidLocation(coordinates)):
        board[coordinates[0]][coordinates[1]] = currentPlayer
        currentPlayer = (currentPlayer + 1) % 2
        turnNumber += 1
    else:
        print("Invalid location")

# checks to see if anyone has won
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

# Checks to see if that board is tied/at a stalemate
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

ticTacGo()