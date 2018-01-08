def main():
    X = "X"
    O = "O"

    state = str(input("Enter inital state below as a \
list without any quotations\n\nInitial State: "))
    turn = str(input("\nEnter who's turn it is (X or O)\
 without any quotations: "))
    state = state.upper()
    turn = turn.upper()

    state = state.split(",")  # uses split to turn string into a list
    state[0], state[-1] = state[0][1], state[-1][0]
    # since there is an extra [ and ]
    # the above removes them

    print("")

    # to avoid errors, only gives the first 9 elements of the list incase user
    # gave more
    temp = TreeBuildAB(state[:9], turn)
    display(temp)  # formats TreeBuildAB output to be displayed nicely


# converts move from tuple to int for indexing the board e.g. (1,1) becomes 4
def tupleToInt(x):
    if x == None:
        return x
    return 3 * x[0] + x[1]


# converts move from int to tuple to properly display coordinates
def intToTuple(x):
    if x == None:
        return x
    a = 0
    while x >= 3:
        a += 1
        x -= 3
    return a, x


# returns a list of all possible playable position (all empty spots)
def moves(board):
    emp = []
    for i in range(len(board)):
        if board[i] == " ":
            emp.append(i)
    return emp[:]


def TreeBuildAB(S, player):
    nextT = "X" if player == "O" else "O"
    empty = moves(S[:])
    result = []
    check, newmove = alphabeta(S[:], player, -100, 100)
    result.append(S[:] + [check] + [player] + [newmove])
    for move in empty[:]:
        S[move] = player
        res = checkWin(S[:])
        if res != " ":
            if res == "X":
                result.append(S[:] + [1] + [nextT] + [None])
            else:
                result.append(S[:] + [-1] + [nextT] + [None])
        else:
            result.append(TreeBuildAB(S[:], nextT))
        S[move] = " "
    return result


def alphabeta(S, player, alpha, beta):
    nextT = "X" if player == "O" else "O"
    win = checkWin(S[:])
    empty = moves(S[:])
    if win == "X":
        return 1, None
    elif win == "O":
        return -1, None
    elif len(empty) == 0:
        return 0, None
    best = None
    for move in empty:
        S[move] = player
        check, newmove = alphabeta(S[:], nextT, alpha, beta)
        S[move] = " "
        if player == "X":
            if check > alpha:
                alpha = check
                best = intToTuple(move)
            if alpha >= beta:
                return beta, best
        else:
            if check < beta:
                beta = check
                best = intToTuple(move)
            if beta <= alpha:
                return alpha, best
    if player == "X":
        return alpha, best
    else:
        return beta, best


# checks if X or O has won, returns their letter, if not return " "
def checkWin(board):
    for i in range(3):
        if board[3 * i] == board[(3 * i) + 1] == board[(3 * i) + 2] and board[3 * i] != " ":
            return board[3 * i][:]
        elif board[i] == board[i + 3] == board[i + 6] and board[i] != " ":
            return board[i][:]
        elif (board[0] == board[4] == board[8] or board[2] == board[4] == board[6]) and board[4] != " ":
            return board[4][:]
    return " "


def print_board(board):  # displays the state like a tic tac toe game board
    board = board[:9]
    x = "---+---+---"
    print(("\n {0[0]} | {0[1]} | {0[2]}\n{1}\n {0[3]} | {0[4]} | {0[5]}\n\
{1}\n {0[6]} | {0[7]} | {0[8]}\n".format(board[:], x)))


def display(S):  # formats TreeBuildAB list to display in correct format
    Q = []
    for i in S[:]:
        if len(i[:]) >= 1 and len(i[:]) <= 10:
            Q.append(display(i[:]))
        else:  # Philip said to include Player and Move as well, not just State and Value
            print("State=[{0[0]},{0[1]},{0[2]},\
{0[3]},{0[4]},{0[5]},{0[6]},{0[7]},{0[8]}], Value={0[9]}\
, Player={0[10]}, Move={0[11]}".format(i[:]))
#            print("State=[{0[0]},{0[1]},{0[2]},\
# {0[3]},{0[4]},{0[5]},{0[6]},{0[7]},{0[8]}], Value={0[9]}".format(i[:]))
    return Q[:]


def test():
    a, b = -100, 100
    assert alphabeta(list("X    O XO"), "X", a, b) == (1, intToTuple(2))
    assert alphabeta(list("OXX   XOO"), "X", a, b) == (1, intToTuple(4))
    assert alphabeta(list("XX   OO O"), "X", a, b) == (1, intToTuple(2))
    assert alphabeta(list("XXOOO XO "), "X", a, b) == (0, intToTuple(5))
    assert alphabeta(list("OO XXO XO"), "X", a, b) == (0, intToTuple(2))
    assert alphabeta(list("XX OO XO "), "O", a, b) == (-1, intToTuple(5))
    assert alphabeta(list("XX  O XOO"), "O", a, b) == (1, intToTuple(2))
    return "Test cases passed"

main()
