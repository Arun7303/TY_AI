import math


def create_board():
    return [[' ' for _ in range(3)] for _ in range(3)]


def print_board(board):
    for row in board:
        print('|'.join(row))
        print('-' * 5)


def check_winner(board):
    
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    
    return None


def is_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True


def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    elif is_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score


def find_best_move(board):
    best_score = -math.inf
    move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move


def play_game():
    board = create_board()
    print("Tic Tac Toe (You are 'O')\n")
    print_board(board)

    while True:
        
        row = int(input("Enter row (0, 1, 2): "))
        col = int(input("Enter column (0, 1, 2): "))

        if board[row][col] != ' ':
            print("Invalid move. Try again.")
            continue
        board[row][col] = 'O'

        print_board(board)

        if check_winner(board) == 'O':
            print("You win!")
            break
        if is_full(board):
            print("It's a draw!")
            break

        
        print("AI's move:")
        move = find_best_move(board)
        if move:
            board[move[0]][move[1]] = 'X'
            print_board(board)

        if check_winner(board) == 'X':
            print("AI wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break


if __name__ == "__main__":
    play_game()
