import tkinter as tk
from tkinter import messagebox
import random
import copy

class TicTacToe:
    def __init__(self, mode, difficulty, main_root):
        self.mode = mode
        self.difficulty = difficulty
        self.main_root = main_root
        self.root = tk.Toplevel()
        self.root.title(f"Tic-Tac-Toe - {self.difficulty} Mode")
        self.root.configure(bg="#222831")
        self.current_player = "X"
        self.board = [[None]*3 for _ in range(3)]
        self.buttons = []

        title = tk.Label(self.root, text=f"Tic-Tac-Toe: {self.mode} - {self.difficulty}", 
                         font=("Helvetica", 22, "bold"), fg="#eeeeee", bg="#222831")
        title.grid(row=0, column=0, columnspan=3, pady=10)

        for row in range(3):
            button_row = []
            for col in range(3):
                btn = tk.Button(
                    self.root, text="", font=("Helvetica", 36, "bold"),
                    width=4, height=2, bg="#393e46", fg="#eeeeee", activebackground="#00adb5",
                    command=lambda r=row, c=col: self.on_click(r, c)
                )
                btn.grid(row=row + 1, column=col, padx=8, pady=8)
                button_row.append(btn)
            self.buttons.append(button_row)

    def on_click(self, row, col):
        if self.board[row][col] is None:
            self.make_move(row, col, self.current_player)

            if self.check_winner(self.current_player):
                self.highlight_win(self.current_player)
                messagebox.showinfo("Game Over", f"🎉 Player {self.current_player} wins!")
                self.end_game()
                return
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.end_game()
                return

            if self.mode == "PVC" and self.current_player == "X":
                self.current_player = "O"
                self.root.after(400, self.computer_move)
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def make_move(self, row, col, player):
        self.board[row][col] = player
        color = "#00adb5" if player == "X" else "#ff5722"
        self.buttons[row][col].config(text=player, fg=color)

    def empty_cells(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] is None]

    def computer_move(self):
        if self.difficulty == "Easy":
            r, c = random.choice(self.empty_cells())
        elif self.difficulty == "Medium":
            r, c = self.medium_move()
        else:
            _, move = self.minimax(copy.deepcopy(self.board), "O")
            r, c = move

        self.make_move(r, c, "O")

        if self.check_winner("O"):
            self.highlight_win("O")
            messagebox.showinfo("Game Over", "💻 Computer wins!")
            self.end_game()
        elif self.is_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.end_game()
        else:
            self.current_player = "X"

    def medium_move(self):
        for r, c in self.empty_cells():
            self.board[r][c] = "O"
            if self.check_winner("O"):
                self.board[r][c] = None
                return (r, c)
            self.board[r][c] = None

        for r, c in self.empty_cells():
            self.board[r][c] = "X"
            if self.check_winner("X"):
                self.board[r][c] = None
                return (r, c)
            self.board[r][c] = None

        if self.board[1][1] is None:
            return (1, 1)

        for r, c in [(0,0), (0,2), (2,0), (2,2)]:
            if self.board[r][c] is None:
                return (r, c)

        return random.choice(self.empty_cells())

    def minimax(self, board, player):
        if self.evaluate(board) == 1:
            return (1, None)
        if self.evaluate(board) == -1:
            return (-1, None)
        if all(all(cell is not None for cell in row) for row in board):
            return (0, None)

        if player == "O":
            best = -float("inf")
            best_move = None
            for r, c in self.empty_cells_on_board(board):
                board[r][c] = "O"
                score, _ = self.minimax(board, "X")
                board[r][c] = None
                if score > best:
                    best = score
                    best_move = (r, c)
            return best, best_move
        else:
            best = float("inf")
            best_move = None
            for r, c in self.empty_cells_on_board(board):
                board[r][c] = "X"
                score, _ = self.minimax(board, "O")
                board[r][c] = None
                if score < best:
                    best = score
                    best_move = (r, c)
            return best, best_move

    def empty_cells_on_board(self, board):
        return [(r,c) for r in range(3) for c in range(3) if board[r][c] is None]

    def evaluate(self, board):
        for row in board:
            if row == ["O"]*3:
                return 1
            if row == ["X"]*3:
                return -1
        for col in range(3):
            if [board[r][col] for r in range(3)] == ["O"]*3:
                return 1
            if [board[r][col] for r in range(3)] == ["X"]*3:
                return -1
        if [board[i][i] for i in range(3)] == ["O"]*3:
            return 1
        if [board[i][i] for i in range(3)] == ["X"]*3:
            return -1
        if [board[i][2 - i] for i in range(3)] == ["O"]*3:
            return 1
        if [board[i][2 - i] for i in range(3)] == ["X"]*3:
            return -1
        return 0

    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[r][col] == player for r in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def highlight_win(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                for j in range(3):
                    self.buttons[i][j].config(bg="#00ff00")
                return
            if all(self.board[j][i] == player for j in range(3)):
                for j in range(3):
                    self.buttons[j][i].config(bg="#00ff00")
                return
        if all(self.board[i][i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][i].config(bg="#00ff00")
            return
        if all(self.board[i][2 - i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][2 - i].config(bg="#00ff00")
            return

    def is_draw(self):
        return all(all(cell is not None for cell in row) for row in self.board)

    def end_game(self):
        self.root.destroy()
        self.main_root.deiconify()

def start_menu():
    main_root = tk.Tk()
    main_root.title("Tic-Tac-Toe Menu")
    main_root.configure(bg="#222831")

    tk.Label(main_root, text="Choose Game Mode", font=("Helvetica", 24, "bold"), fg="#eeeeee", bg="#222831").pack(pady=10)

    tk.Button(main_root, text="You vs Computer", font=("Helvetica", 18), width=20, bg="#00adb5", fg="#eeeeee",
              command=lambda: select_difficulty(main_root)).pack(pady=10)

    tk.Button(main_root, text="You vs Person", font=("Helvetica", 18), width=20, bg="#393e46", fg="#eeeeee",
              command=lambda: [main_root.withdraw(), TicTacToe("PVP", "Medium", main_root)]).pack(pady=10)

    tk.Button(main_root, text="Exit", font=("Helvetica", 18), width=20, bg="#ff5722", fg="#eeeeee",
              command=main_root.quit).pack(pady=10)

    main_root.mainloop()

def select_difficulty(main_root):
    diff_win = tk.Toplevel()
    diff_win.title("Select Difficulty")
    diff_win.configure(bg="#222831")

    tk.Label(diff_win, text="Select Difficulty", font=("Helvetica", 20, "bold"), fg="#eeeeee", bg="#222831").pack(pady=10)

    for level in ["Easy", "Medium", "Hard"]:
        tk.Button(diff_win, text=level, font=("Helvetica", 16), width=15, bg="#00adb5", fg="#eeeeee",
                  command=lambda l=level: [main_root.withdraw(), diff_win.destroy(), TicTacToe("PVC", l, main_root)]).pack(pady=5)

    tk.Button(diff_win, text="⬅ Back", font=("Helvetica", 16), width=15, bg="#393e46", fg="#eeeeee",
              command=lambda: [diff_win.destroy(), main_root.deiconify()]).pack(pady=10)

if __name__ == "__main__":
    start_menu()
