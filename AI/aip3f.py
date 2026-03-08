import math

HUMAN_PLAYER = 'X'
AI_PLAYER = 'O'
EMPTY = ' '

# Print Board
def print_board(board):
    for i in range(3):
        row = board[i * 3:(i + 1) * 3]
        print(' | '.join(row))
        if i < 2:
            print('-' * 9)

# Check Win
def check_win(board, player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],      # Horizontal
        [0,3,6], [1,4,7], [2,5,8],      # Vertical
        [0,4,8], [2,4,6]                # Diagonal
    ]

    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

# Check Game Over
def is_game_over(board):
    return check_win(board, HUMAN_PLAYER) or \
           check_win(board, AI_PLAYER) or \
           EMPTY not in board

# Get Empty Cells
def get_empty_cells(board):
    return [i for i, spot in enumerate(board) if spot == EMPTY]

# Minimax with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, is_maximizing):

    if check_win(board, AI_PLAYER):
        return 10 - depth
    if check_win(board, HUMAN_PLAYER):
        return depth - 10
    if EMPTY not in board:
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for cell in get_empty_cells(board):
            board[cell] = AI_PLAYER
            eval = minimax(board, depth + 1, alpha, beta, False)
            board[cell] = EMPTY
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = math.inf
        for cell in get_empty_cells(board):
            board[cell] = HUMAN_PLAYER
            eval = minimax(board, depth + 1, alpha, beta, True)
            board[cell] = EMPTY
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Find Best Move for AI
def find_best_move(board):
    best_eval = -math.inf
    best_move = -1

    for cell in get_empty_cells(board):
        board[cell] = AI_PLAYER
        eval = minimax(board, 0, -math.inf, math.inf, False)
        board[cell] = EMPTY

        if eval > best_eval:
            best_eval = eval
            best_move = cell

    return best_move

# Main Function
def main():
    board = [EMPTY] * 9
    current_player = HUMAN_PLAYER

    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while not is_game_over(board):

        if current_player == HUMAN_PLAYER:
            try:
                move = int(input("Player X, Enter your move (0-8): "))
                if move in get_empty_cells(board):
                    board[move] = HUMAN_PLAYER
                    current_player = AI_PLAYER
                else:
                    print("Invalid move! Try again.")
            except ValueError:
                print("Invalid input! Enter number between 0 and 8.")
        else:
            print("AI is thinking...")
            move = find_best_move(board)
            board[move] = AI_PLAYER
            print(f"AI chose position: {move}")
            current_player = HUMAN_PLAYER

        print_board(board)

    # Final Result
    if check_win(board, HUMAN_PLAYER):
        print("Player X wins!")
    elif check_win(board, AI_PLAYER):
        print("AI wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()
