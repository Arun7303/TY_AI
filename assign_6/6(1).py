import itertools
import tkinter as tk
from tkinter import messagebox

def get_unique_letters(operands, result):
    return set(''.join(operands) + result)

def to_number(word, letter_to_digit):
    return int(''.join(str(letter_to_digit[char]) for char in word))

def solve_cryptarithmetic(expression):
    if '+' not in expression or '=' not in expression:
        return "Invalid input format."

    left, result = expression.split('=')
    operands = [word.strip() for word in left.split('+')]
    result = result.strip()

    # Get all unique letters
    letters = list(get_unique_letters(operands, result))
    if len(letters) > 10:
        return "Too many unique letters (>10). Cannot assign unique digits."

    leading_letters = set(word[0] for word in operands + [result])
    digits = range(10)

    for perm in itertools.permutations(digits, len(letters)):
        letter_to_digit = dict(zip(letters, perm))

        # No leading zero allowed
        if any(letter_to_digit[ch] == 0 for ch in leading_letters):
            continue

        # Convert words to numbers
        operand_values = [to_number(word, letter_to_digit) for word in operands]
        result_value = to_number(result, letter_to_digit)

        if sum(operand_values) == result_value:
            solution = f"\nSolution Found:\n"
            for k in sorted(letter_to_digit.keys()):
                solution += f"{k} = {letter_to_digit[k]}\n"
            solution += "\nCheck:\n"
            solution += " + ".join(str(val) for val in operand_values) + " = " + str(result_value)
            return solution

    return "No solution found."

class CryptarithmeticSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptarithmetic Solver")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter Cryptarithmetic Expression (e.g., SEND + MORE = MONEY):", font=("Arial", 12)).pack(pady=10)

        self.expression_entry = tk.Entry(self.root, width=40, font=('Arial', 14))
        self.expression_entry.pack(pady=10)

        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve_expression, font=("Arial", 12), bg="lightblue")
        self.solve_button.pack(pady=10)

        self.result_text = tk.Text(self.root, height=10, width=50, font=("Arial", 12))
        self.result_text.pack(pady=10)

    def solve_expression(self):
        expression = self.expression_entry.get().strip()
        result = solve_cryptarithmetic(expression)
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

def run_gui():
    root = tk.Tk()
    app = CryptarithmeticSolverGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
