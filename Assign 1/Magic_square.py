import tkinter as tk
from tkinter import messagebox, simpledialog

class MagicSquareGUI:
    def __init__(self, n, magic_sum):
        if n < 3 or n % 2 == 0:
            raise ValueError("Magic squares are only defined for odd numbers greater than or equal to 3.")
        
        self.n = n
        self.magic_sum = magic_sum
        self.square = [[0] * n for _ in range(n)]
        self.root = tk.Tk()
        self.root.title(f"{n}x{n} Magic Square with Sum {magic_sum}")
        
        self.create_magic_square()
        self.adjust_to_magic_sum()
        self.setup_gui()

    def create_magic_square(self):
        n = self.n
        num = 1
        i, j = 0, n // 2

        while num <= n ** 2:
            self.square[i][j] = num
            num += 1

            new_i = (i - 1) % n
            new_j = (j + 1) % n

            if self.square[new_i][new_j]:
                i += 1
            else:
                i, j = new_i, new_j

    def adjust_to_magic_sum(self):
        """Scales the base magic square to match the user-specified magic sum."""
        base_sum = self.n * (self.n ** 2 + 1) // 2  # Standard magic sum formula
        factor = self.magic_sum / base_sum

        for i in range(self.n):
            for j in range(self.n):
                self.square[i][j] = int(self.square[i][j] * factor)

    def setup_gui(self):
        for i in range(self.n):
            for j in range(self.n):
                tk.Label(self.root, text=self.square[i][j], font=("Arial", 18), 
                         borderwidth=2, relief="solid", width=4, height=2).grid(row=i, column=j)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    n = 3  # You can change this value for larger magic squares
    try:
        magic_sum = simpledialog.askinteger("Input", f"Enter the desired sum for {n}x{n} magic square:")
        
        if magic_sum is None:
            raise ValueError("No sum provided.")
        
        app = MagicSquareGUI(n, magic_sum)
        app.run()
    except ValueError as e:
        messagebox.showerror("Error", str(e))
