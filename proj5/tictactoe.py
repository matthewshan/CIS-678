import random
# [ col 1: [row top, mid, bottom], col 2, col 3 ]
# Thus, coordinates must be list[col][row], like the board
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
# Keys = integer version of the board, value is the q value (or whatever is needed)
rewardDict = {}
valueDict = {}

boardHistory = []

currentPlayer = 1
# Not sure if needed, but our "time" for Q learning. Increments by 1 every time someone makes a move
turnNumber = 0

LEARNING_RATE = 0.5
DISCOUNT_RATE = 0.9

def feedReward(reward):
    global LEARNING_RATE, DISCOUNT_RATE, valueDict
    # Starting with the last move (not including potential moves after the final state)
    moveIndex = len(boardHistory) - 2
    # Start at the end of the game and work your way back
    for state, action in reversed(boardHistory):
        # Initialize the values for the keys if they don't exist
        if (state not in valueDict):
            valueDict[state] = {}
        if (action not in valueDict[state]):
            valueDict[state][action] = 0
        # Need to find the next best move from the passed in state
            # valueDict = {
            #     "111222333":{
            #         (1, 2): 1
            #     }
            # }
        # Get a list of all the coordinates at which someone could place a piece
        validSpaces = returnValidSpaces()
        # t + 1
        # Find the next best move that could be taken
        maxValue = 0
        for nextAction in validSpaces:
            # Generate our t+1 state using the current state and given action
            newState = generateState(state, nextAction, moveIndex)
            if (newState not in valueDict):
                valueDict[newState] = {}
            if (nextAction not in valueDict[newState]):
                valueDict[newState][nextAction] = 0
            if (valueDict[newState][nextAction] > maxValue):
                maxValue = valueDict[newState][nextAction]
        # Q(s,a) = Q(s,a) + LR(r+y*maxQ(s+1, a+1) - Q(s,a))
        valueDict[state][action] = valueDict[state][action] + LEARNING_RATE * (reward + DISCOUNT_RATE * maxValue - valueDict[state][action])
        # Move on to the next most recent move, repeat until finished
        moveIndex-= 1

def getBestMove(playerNum):
    global board
    validSpaces = returnValidSpaces()
    # t + 1
    # Find the next best move that could be taken
    maxValue = 0
    bestAction = None
    for nextAction in validSpaces:
        # Generate our t+1 state using the current state and given action
        newState = generateState(translateBoard(board), nextAction, playerNum + 1)
        if (newState not in valueDict):
            valueDict[newState] = {}
        if (nextAction not in valueDict[newState]):
             valueDict[newState][nextAction] = 0
        if (valueDict[newState][nextAction] > maxValue):
            maxValue = valueDict[newState][nextAction]
            bestAction = nextAction
    if (bestAction == None):
        # Pick a random move
        bestAction = validSpaces[random.randint(0, len(validSpaces)-1)]

    return bestAction

def generateState(state, nextAction, moveNum):
    # If even number move, p1 did the move. else p2 did the move
    index = nextAction[0] * 3 + nextAction[1]
    result = ''
    for i in range(len(state)):
        if (i == index):
            result += str((moveNum % 2) + 1)
        else:
            result += state[i]
    # state[index] = str((moveNum % 2) + 1
    return result

# This is where we will do all the stuff with Q learning and whatnot
def ticTacGo():
    global board, turnNumber, currentPlayer, boardHistory
    winCount = [0, 0]
    gameCount = 0
    totalTies = 0
    AI_PLAYER = 1
    while (gameCount < 1000):
        if currentPlayer == AI_PLAYER:
            aiMove = getBestMove(currentPlayer)
            boardHistory.append((translateBoard(board), aiMove))
            doTurn(aiMove)
        else:
            validMoves = returnValidSpaces()
            enemyMove = validMoves[random.randint(0, len(validMoves)-1)]
            # boardHistory.append((translateBoard(board), enemyMove))
            doTurn(enemyMove)

        if (hasWon(AI_PLAYER)):
            winCount[AI_PLAYER - 1] += 1
            gameCount += 1
            print ("Player " + str(AI_PLAYER) + " won game " + str(gameCount) + " after " + str(turnNumber) + " total moves.")
            print("--Total wincount--")
            print ("Player 1: " + str(winCount[0]))
            print("Player 2: " + str(winCount[1]))
            print("Total ties: " + str(totalTies) + "\n")
            feedReward(10)
            resetBoard()
        elif (hasWon((AI_PLAYER % 2) + 1)):
            winCount[((AI_PLAYER % 2) + 1) - 1] += 1
            gameCount += 1
            print ("Player " + str((AI_PLAYER % 2) + 1) + " won game " + str(gameCount) + " after " + str(turnNumber) + " total moves.")
            print("--Total wincount--")
            print ("Player 1: " + str(winCount[0]))
            print("Player 2: " + str(winCount[1]))
            print("Total ties: " + str(totalTies) + "\n")
            feedReward(-1)
            resetBoard()
        elif (checkTie()):
            totalTies += 1
            gameCount += 1
            print ("Game " + str(gameCount) + " has ended in a tie after " + str(turnNumber) + " total moves.")
            print("--Total wincount--")
            print ("Player 1: " + str(winCount[0]))
            print("Player 2: " + str(winCount[1]))
            print("Total ties: " + str(totalTies) + "\n")
            feedReward(1.5*AI_PLAYER)
            resetBoard()
    # global turnNumber, currentPlayer, boardHistory
    # winCount = [0, 0]
    # gameCount = 0
    # totalTies = 0
    # while (gameCount < 1000):
    #     currPlay = currentPlayer
    #     row = random.randint(0,2)
    #     col = random.randint(0,2)
    #     didTurn = False
    #     # This if isn't needed, but just so we don't get a bunch of prints
    #     if (isValidLocation([col, row])):
    #         doTurn([col, row])
    #         boardHistory.append((translateBoard(board), (col, row)))
    #         didTurn = True
    #     if (didTurn):
    #         # If the player who did a move won
    #         if (hasWon(currPlay)):
    #             winCount[currPlay - 1] += 1
    #             gameCount += 1
    #             print ("Player " + str(currPlay) + " won game " + str(gameCount) + " after " + str(turnNumber) + " total moves.")
    #             print("--Total wincount--")
    #             print ("Player 1: " + str(winCount[0]))
    #             print("Player 2: " + str(winCount[1]))
    #             print("Total ties: " + str(totalTies) + "\n")
    #             resetBoard()
    #         elif (checkTie()):
    #             totalTies += 1
    #             gameCount += 1
    #             print ("Game " + str(gameCount) + " has ended in a tie after " + str(turnNumber) + " total moves.")
    #             print("--Total wincount--")
    #             print ("Player 1: " + str(winCount[0]))
    #             print("Player 2: " + str(winCount[1]))
    #             print("Total ties: " + str(totalTies) + "\n")
    #             resetBoard()


# Resets the board to be all empty
def resetBoard():
    global board, currentPlayer, turnNumber, boardHistory
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    currentPlayer = 1
    turnNumber = 0
    boardHistory = []

# Translates the board from a 2D array to a 9 number long string.
# should be col 111222333 for the format, with 111 being top to bottom of col 1
# 1 2 3
# 1 2 3
# 1 2 3
def translateBoard(boardState):
    global board
    numberString = ""
    for col in range(3):
        for row in range(3):
            numberString += str(board[col][row])
    return numberString

# Gets the value of a specific board state, reward, etc
def getStateValue(boardState):
    global stateDict
    translatedState = translateBoard(boardState)
    try:
        return stateDict[translatedState]
    except:
        print("Could not find board state.")
        return None

# Sets the value of a specific board state, reward, etc
def setStateValue(boardState, val):
    global stateDict
    stateDict[translateBoard(boardState)] = val

# Returns a list of tuples of all unused places on the board
def returnValidSpaces():
    global board
    validLocations = []
    # Rows and cols, 0, 1, 2
    for col in range(3):
        for row in range(3):
            if (board[col][row] == 0):
                validLocations.append((col, row))
    return validLocations

# Checks to see if the given [col, row] coordinates are valid
def isValidLocation(coordinates):
    global board
    if (board[coordinates[0]][coordinates[1]] == 0):
        return True
    return False

# Puts a piece at the given coordinates for the current player
def doTurn(coordinates):
    global currentPlayer, board, turnNumber
    if (isValidLocation(coordinates)):
        board[coordinates[0]][coordinates[1]] = currentPlayer
        currentPlayer = ((currentPlayer + 2) % 2) + 1
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
            if (board[col][row] == 0):
                foundEmptySpace = True
    if (not foundEmptySpace and not hasWon(0) and not hasWon(1)):
        return True
    return False

def calculateReward(learningPlayer):
    if (hasWon(currentPlayer)):
        return 1
    elif (hasWon((currentPlayer % 2) + 1)):
        return 0
    elif (checkTie()):
        return 0.5

ticTacGo()