import math
E, AI, H = "_", "X", "O"

def win(b):
    for a,c,d in [(0,1,2),(3,4,5),(6,7,8),
                  (0,3,6),(1,4,7),(2,5,8),
                  (0,4,8),(2,4,6)]:
        if b[a]==b[c]==b[d]!=E: return b[a]

def terminal(b): return win(b) or E not in b


def evaluate(b):
    w = win(b)
    if w==AI: return 10
    elif w==H: return -10
    return 0

def alpha_beta(b, maxing, alpha=-math.inf, beta=math.inf):
    if terminal(b): return evaluate(b)
    if maxing:
        best = -math.inf
        for i in range(9):
            if b[i]==E:
                b[i]=AI
                best = max(best, alpha_beta(b, False, alpha, beta))
                b[i]=E
                alpha = max(alpha, best)
                if beta <= alpha: break
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i]==E:
                b[i]=H
                best = min(best, alpha_beta(b, True, alpha, beta))
                b[i]=E
                beta = min(beta, best)
                if beta <= alpha: break
        return best

def best_move(b):
    move, best_score = -1, -math.inf
    for i in range(9):
        if b[i]==E:
            b[i]=AI
            score = alpha_beta(b, False)
            b[i]=E
            if score > best_score:
                best_score, move = score, i
    return move

def print_board(b):
    for i in range(0, 9, 3):
        print(b[i], b[i+1], b[i+2])
    print()  

board = [E]*9
print("Positions are numbered 1-9 as:")
print("1 2 3\n4 5 6\n7 8 9\n")

while not terminal(board):
    print_board(board)

    human = int(input("Your move (1-9): "))-1
    if board[human]==E:
        board[human]=H
    
    if not terminal(board):
        ai = best_move(board)
        print("AI moves to:", ai+1)
        board[ai]=AI

print_board(board)
w = win(board)
print("Winner:", w if w else "Draw")