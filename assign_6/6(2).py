import tkinter as tk

def solve_crossword(grid, words):
    for word in words:
        placed = False
        for i in range(len(grid)):
            for j in range(len(grid[0]) - len(word) + 1):
                # Check if the word fits horizontally
                if all(grid[i][j+k] == '-' for k in range(len(word))):
                    for k in range(len(word)):
                        grid[i][j+k] = word[k]
                    placed = True
                    break
            if placed:
                break
    return grid

def show_crossword(grid):
    root = tk.Tk()
    root.title("Crossword Puzzle")

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            cell = tk.Entry(root, width=3, justify='center', font=('Arial', 14))
            cell.grid(row=i, column=j, padx=2, pady=2)
            cell.insert(0, grid[i][j])
            cell.config(state='readonly')
    root.mainloop()

def main():
    print("Enter 5 rows of crossword grid (use '-' for empty, '+' for block):")
    grid = []
    for _ in range(5):
        row = input().strip()
        grid.append(list(row))

    words_input = input("Enter words separated by commas: ").strip()
    words = [word.strip().upper() for word in words_input.split(',')]

    solved_grid = solve_crossword(grid, words)
    show_crossword(solved_grid)

if __name__ == "__main__":
    main()
