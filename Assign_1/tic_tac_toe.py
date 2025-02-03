import tkinter as tk
from tkinter import messagebox


root = tk.Tk()
root.title("Tic Tac Toe")


current_player = "X"
board = ["" for _ in range(9)]  


def check_winner():
    
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  
        (0, 4, 8), (2, 4, 6)              
    ]

    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != "":
            return board[combo[0]]

    if "" not in board:
        return "Draw"

    return None


def on_click(index):
    global current_player

    if board[index] == "":
        board[index] = current_player
        buttons[index]["text"] = current_player

        winner = check_winner()

        if winner:
            if winner == "Draw":
                messagebox.showinfo("Game Over", "It's a Draw!")
            else:
                messagebox.showinfo("Game Over", f"Player {winner} wins!")
            reset_game()
        else:
            
            current_player = "O" if current_player == "X" else "X"


def reset_game():
    global current_player, board
    current_player = "X"
    board = ["" for _ in range(9)]
    for button in buttons:
        button["text"] = ""


buttons = []
for i in range(9):
    btn = tk.Button(root, text="", font=("Arial", 24), height=2, width=5,
                     command=lambda idx=i: on_click(idx))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)


root.mainloop()
