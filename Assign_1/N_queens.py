import tkinter as tk
from tkinter import messagebox

class NQueensGUI:
    def __init__(self, n):
        self.n = n
        self.root = tk.Tk()
        self.root.title(f"{n}-Queens Problem")
        self.board = [[0] * n for _ in range(n)]
        self.buttons = [[None for _ in range(n)] for _ in range(n)]
        self.setup_board()

    def setup_board(self):
        for row in range(self.n):
            for col in range(self.n):
                btn = tk.Button(self.root, width=4, height=2, bg="white",
                                command=lambda r=row, c=col: self.toggle_queen(r, c))
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn

    def toggle_queen(self, row, col):
        if self.board[row][col] == 1:
            self.board[row][col] = 0
            self.buttons[row][col].config(text="", bg="white")
        else:
            if self.is_safe(row, col):
                self.board[row][col] = 1
                self.buttons[row][col].config(text="Q", bg="lightblue")
                if self.check_solution():
                    messagebox.showinfo("Success", "All queens are placed safely!")
            else:
                messagebox.showwarning("Invalid Move", "This position is not safe!")

    def is_safe(self, row, col):
        for i in range(self.n):
            if self.board[row][i] == 1 or self.board[i][col] == 1:
                return False

        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False

        for i, j in zip(range(row, -1, -1), range(col, self.n)):
            if self.board[i][j] == 1:
                return False

        return True

    def check_solution(self):
        queens = sum(row.count(1) for row in self.board)
        return queens == self.n

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    n = 4  
    app = NQueensGUI(n)
    app.run()
