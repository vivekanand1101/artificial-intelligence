def same_row_count(n, matrix, player):
    min_across_rows = float("inf")
    for i in range(n):
        count = 0
        for j in range(n):
            if (str(matrix[(i * n) + j]) != str(player)) and (str(matrix[(i * n) + j]) != '*'):
                count = float("inf")
            elif str(matrix[(i * n) + j]) == '*':
                count += 1
        if count < min_across_rows:
            min_across_rows = count
    return min_across_rows

def same_col_count(n, matrix, player):
    min_across_cols = float("inf")
    for i in range(n):
        count = 0
        for j in range(n):
            if (str(matrix[(j * n) + i]) != str(player)) and (str(matrix[(j * n) + i]) != '*'):
                count = float("inf")
            elif str(matrix[(j * n) + i]) == '*':
                count += 1
        if count < min_across_cols:
            min_across_cols = count
    return min_across_cols

def forward_diagonal_count(n, matrix, player):
    count = 0
    for i in range(n):
        if (str(matrix[(n - 1) * (i + 1)]) != str(player)) and (str(matrix[(n - 1) * (i + 1)]) != '*'):
            #print 'player %s index %s ' % (player, (n - 1) * (i + 1))
            return float("inf")
        if (str(matrix[(n - 1) * (i + 1)]) == '*'):
            count += 1
    return count

def backward_diagonal_count(n, matrix, player):
    count = 0
    for i in range(n):
        if (str(matrix[(n + 1) * i]) != str(player)) and (str(matrix[(n + 1) * i]) != '*'):
            return float("inf")
        if (str(matrix[(n + 1) * i]) == '*'):
            count += 1
    return count

def min_moves_for_a_player_to_win(n, matrix, player):
    min_to_win = min([
                        same_row_count(n, matrix, player),
                        same_col_count(n, matrix, player),
                        forward_diagonal_count(n, matrix, player),
                        backward_diagonal_count(n, matrix, player)
                    ])
    return min_to_win

def check_turn(count1, count2):
    if count1 > count2:
        return '2'
    else:
        return '1'

def calculate_min_steps(n, matrix):
    count_player_1_moves = matrix.count('1')
    count_player_2_moves = matrix.count('2')
    turn = check_turn(count_player_1_moves, count_player_2_moves)
    min_moves_for_player_1_to_win = min_moves_for_a_player_to_win(n, matrix, '1')
    min_moves_for_player_2_to_win = min_moves_for_a_player_to_win(n, matrix, '2')
    if (min_moves_for_player_1_to_win, min_moves_for_player_2_to_win) == (float('inf'), float('inf')):
        return matrix.count('*')
    elif min_moves_for_player_1_to_win == 0 or min_moves_for_player_2_to_win == 0:
        return 0
    diff1 = min_moves_for_player_1_to_win - min_moves_for_player_2_to_win
    diff2 = min_moves_for_player_2_to_win - min_moves_for_player_1_to_win

    blanks_count = matrix.count('*')
    #if diff1 == float("inf") or diff2 == float("inf"):
     #   return blanks_count
    if diff1 == 0:
        return min([2 * min_moves_for_player_1_to_win - 1, blanks_count])
    elif diff1 < 0 and turn == '1':
        return min([2 * min_moves_for_player_1_to_win - 1, blanks_count])
    elif diff1 < 0 and turn == '2':
        return min([2 * min_moves_for_player_1_to_win, blanks_count])
    elif diff1 > 0 and turn == '1':
        return min([2 * min_moves_for_player_2_to_win, blanks_count])
    elif diff1 > 0 and turn == '2':
        return min([2 * min_moves_for_player_2_to_win - 1, blanks_count])

def main():
    t = int(raw_input())
    for i in range(t):
        x = raw_input()
        x = x.split(' ')
        n = int(x[0])
        matrix = x[1]
        min_steps = calculate_min_steps(n, matrix)
        print min_steps

main()
