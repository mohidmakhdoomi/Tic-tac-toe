def AIPlay(board):
    p = whoFirst()
    end = False
    print_board(board[:])
    while end == False:
        aimove = TreeBuildAB(board[:], p)
        aimove = aimove[0][:]
        aimove = aimove[-1]
        print("\nPlayer {0}'s Move: {1}".format(p, aimove))
        move = tupleToInt(aimove)
        board[move] = p[:]
        p = "X" if p == "O" else "O"
        print_board(board[:])
        end = finish(board[:])


def OnePlay(board):
    p = whoFirst()
    end = False
    print_board(board[:])
    print("\nEnter move in this format: \
x,y and with no brackets or quotations\n\n\
Upper-left corner is 1,1 and lower-right is 3,3")
    while end == False:
        if p == "O":
            aimove = TreeBuildAB(board[:], p)
            aimove = aimove[0][:]
            aimove = aimove[-1]
            print("\nPlayer {0}'s Move: {1}".format(p, aimove))
            move = tupleToInt(aimove)
        else:
            row, col = eval(input("\nPlayer {0}'s Move: ".format(p)))
            row -= 1
            col -= 1
            move = tupleToInt((row, col))
            while move not in moves(board):
                print("\nInvalid move try again")
                row, col = eval(input("\nPlayer {0}'s Move: ".format(p)))
                row -= 1
                col -= 1
                move = tupleToInt((row, col))
        board[move] = p[:]
        p = "X" if p == "O" else "O"
        print_board(board[:])
        end = finish(board[:])


def TwoPlay(board):
    p = whoFirst()
    end = False
    print_board(board[:])
    print("\nEnter move in this format: \
x,y and with no brackets or quotations\n\n\
Upper-left corner is 1,1 and lower-right is 3,3")
    while end == False:
        row, col = eval(input("\nPlayer {0}'s Move: ".format(p)))
        row -= 1
        col -= 1
        move = tupleToInt((row, col))
        while move not in moves(board):
            print("\nInvalid move try again")
            row, col = eval(input("\nPlayer {0}'s Move: ".format(p)))
            row -= 1
            col -= 1
            move = tupleToInt((row, col))
        board[move] = p[:]
        p = "X" if p == "O" else "O"
        print_board(board[:])
        end = finish(board[:])


def whoFirst():
    turn = str(input("\nX or O goes first?: "))
    turn = turn.upper()
    while turn != "X" and turn != "O":
        turn = str(input("\nInvalid answer, X or O goes first?: "))
        turn = turn.upper()
    return turn


def finish(board):
    w = checkWin(board[:])
    empty = moves(board[:])
    end = False
    if len(empty) == 0 and w == " ":
        print("\nIt's a tie")
        end = True
    elif w == "X" or w == "O":
        print("\nWinner is {0}!!".format(w))
        end = True
    return end


def main():
    X = "X"
    O = "O"

    mode = int(input("Choose a game mode below, 0-player, 1-player, 2-player\n\
Enter choice as integers 0,1 and 2\n\nGame Mode: "))

    state = str(input("\nEnter tic tac toe inital game state below as a \
list without any quotations\n\nJust press Enter to start a blank game\n\nInitial State: "))
    if state == "":
        state = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    else:
        state = state.upper()
        state = state.split(",")  # uses split to turn string into a list
        # since there is an extra [ and ]
        state[0], state[-1] = state[0][1], state[-1][0]  # this removes them
    if moves(state[:]) == 0:
        w = checkWin(state[:])
        print("\nNo avaliable spaces")
        if w == " ":
            print("\n\nNo one won")
            return
        else:
            print("\n\nWinner is {0}".format(w))
            return
    elif mode == 0:
        AIPlay(state[:])
    elif mode == 1:
        OnePlay(state[:])
    elif mode == 2:
        TwoPlay(state[:])


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

main()
