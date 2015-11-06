def make_list_of_blank_spaces(board):
    """
    :arg board: list containing '1', '*' and '2'
    :return blank_spaces: list containg indices of all blank spaces
    """

    blank_spaces = []
    for i in range(len(board)):
        if board[i] == '*':
            blank_spaces.append(i)
    return blank_spaces

def calculate_next_player(player):
    """
    :arg player: current player who has the chance to play
    :return next_player: The other player
    """

    if player == '1':
        return '2'
    else:
        return '1'

def same_row(n, board, player):
    for i in range(n):
        flag = True
        if str(board[(i * n) + 0]) != '*':
            x = board[(i * n) + 0]
            for j in range(n):
                if str(board[(i * n) + j]) != x:
                    flag = False
            if flag:
                return True
    return False

def same_col(n, board, player):
    for i in range(n):
        flag = True
        if str(board[(0 * n) + i]) != '*':
            x = board[(0 * n) + i]
            for j in range(n):
                if str(board[(j * n) + i]) != x:
                    flag = False
            if flag:
                return True
    return False

def forward_diagonal(n, board, player):
    if str(board[(n - 1) * 1]) != '*':
        x = board[(n - 1) * 1]
        for i in range(n):
            if str(board[(n - 1) * (i + 1)]) != x:
                return False
        return True
    return False

def backward_diagonal(n, board, player):
    if str(board[(n + 1) * 0]) != '*':
        x = board[(n + 1) * 0]
        for i in range(n):
            if str(board[(n + 1) * i]) != x:
                return False
        return True
    return False

def is_winning_combination(n, board, player):
    if same_row(n, board, player) or same_col(n, board, player) or \
        forward_diagonal(n, board, player) or backward_diagonal(n, board, player):
            return True
    else:
        return False

def MiniMax(n, board, player):
    """
    Computes the next move for a player given the current board state and also
    computes if the player will win or not.

    :arg board: list containing '1','*' and '2'
    :arg player: one character string '1' or '2'
    :return willwin: 1 if '1' is in winning state, 0 if the game is draw and -1 if '2' is
                        winning
    :return nextmove: position where the player can play the next move so that the
                         player wins or draws or delays the loss
    """
    if len(set(board)) == 1:
        return 0, n + 1

    next_player = calculate_next_player(player)

    if is_winning_combination(n, board, player):
        #print 'came ', board
        #print player
        if player == '1':
            #return -1, -1
            return -1,-1
        else:
            #print board
            #return 1, -1
            return 1,-1

    if board.count('*') == 0:
        #print 'board * ', board
        return 0, -1

    blank_spaces = make_list_of_blank_spaces(board)

    results = []
    for i in blank_spaces:
        board[i] = player
        #print 'board ', board
        result, move = MiniMax(n, board, next_player)
        #print 'result ', result
        results.append(result)
        board[i] = '*'

    if player == '1':
        return max(results), blank_spaces[results.index(max(results))]
    else:
        return min(results), blank_spaces[results.index(min(results))]

def main():
    t = int(raw_input())
    for i in range(t):
        x = raw_input()
        x = x.split(' ')
        n = int(x[0])
        board = x[1]
        result, next_move = MiniMax(n, list(board), '1')
        print result

main()
