import copy

import numpy as np
import tkinter as tk
from tkinter import messagebox


class Solitaire:
    def __init__(self):
        # 7x7 board with -1 as invalid spaces, 1 as pegs, and 0 as empty
        self.board = np.array([
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1]
        ])

    def display(self):
        print("  0 1 2 3 4 5 6")
        for i, row in enumerate(self.board):
            print(i, " ".join(['.' if cell == -1 else 'O' if cell == 1 else ' ' for cell in row]))

    def is_valid_move(self, x1, y1, x2, y2):
        x_mp = int((x1 + x2)/2)
        y_mp = int((y1 + y2)/2)
        if self.board[y1, x1] != 1 or self.board[y2, x2] != 0 or self.board[y_mp, x_mp] != 1:
            return False
        if not ((x1 == x2 and abs(y1 - y2) == 2.0) or (y1 == y2 and abs(x1 - x2) == 2.0)):
            return False
        return True

    def move(self, x1, y1, x2, y2):
        x_mp = int((x1 + x2)/2)
        y_mp = int((y1 + y2)/2)
        if self.is_valid_move(x1, y1, x2, y2):
            self.board[y1, x1] = 0
            self.board[y2, x2] = 1
            self.board[y_mp, x_mp] = 0
            return True
        return False

    def successor(self, pos):
        suc = copy.deepcopy(self)
        suc.move(*pos)
        return suc

    def is_game_over(self):
        for y in range(7):
            for x in range(7):
                if self.board[y, x] == 1:
                    for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                        if 0 <= x + dx < 7 and 0 <= y + dy < 7 and self.is_valid_move(x, y, x + dx, y + dy):
                            return False
        return True
    def get_all_moves(self):
        moves = []
        for y in range(7):
            for x in range(7):
                if self.board[y, x] == 1:
                    for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                        if 0 <= x + dx < 7 and 0 <= y + dy < 7 and self.is_valid_move(x, y, x + dx, y + dy):
                            moves.append((x, y, x + dx, y+dy))
        return moves

class SolitaireGUI:
    width = 550
    height = 550
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")

        self.game = Solitaire()
        self.canvas = tk.Canvas(root, width= SolitaireGUI.width, height=SolitaireGUI.height, bg="white")
        self.board_radius = 220  # Radius of the circular board
        self.peg_radius = 15  # Radius of each peg
        self.center_x, self.center_y = SolitaireGUI.width/2, SolitaireGUI.height/2  # Center of the board
        self.canvas.pack()
        self.selected = None

        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def game_restart(self):
        self.game= Solitaire()
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        # Draw wooden circular board
        self.canvas.create_oval(
            self.center_x - self.board_radius, self.center_y - self.board_radius,
            self.center_x + self.board_radius, self.center_y + self.board_radius,
            fill="burlywood", outline="black"
        )
        self.draw_pegs()
    def draw_pegs(self):
        self.canvas.delete("pegs")
        cell_size = 50
        for y in range(7):
            for x in range(7):
                value = self.game.board[y, x]
                if value == -1:
                    continue # skip invalid positions
                x1, y1 = self.center_x + (x - 3) * cell_size,self.center_y + (y - 3) * cell_size

                if value == 0: # empty holes
                    self.canvas.create_oval(x1 + self.peg_radius, y1 + self.peg_radius, x1 - self.peg_radius, y1 - self.peg_radius, outline="black", tags="pegs")

                if value == 1: # pegs
                    peg_color = "red" if self.selected == (x, y) else "saddlebrown"
                    self.canvas.create_oval(x1 + self.peg_radius, y1 + self.peg_radius, x1 - self.peg_radius, y1 - self.peg_radius, fill=peg_color, tags="pegs")

    def successor(self, pos):
        suc = copy.deepcopy(self.game)
        suc.move(*pos)
        return suc

    def on_click(self, event):
        cell_size = 50
        x = round((event.x - self.center_x) / cell_size) + 3
        y = round((event.y - self.center_y) / cell_size) + 3
        self.move(x, y)


    def move(self, x, y):
        if self.selected is None:
            if self.game.board[y, x] == 1:
                self.selected = (x, y)
                self.draw_pegs()
        else:
            x1, y1 = self.selected
            if x1 == x and y1 == y:
                self.selected = None
            elif not self.game.move(x1, y1, x, y):
                print("Invalid move. Try again.")
                print(self.game.board)
                print(self.game.get_all_moves())
            self.selected = None
            self.draw_pegs()
            if self.game.is_game_over():
                messagebox.showinfo("Game Over", "No more moves available!")
    def update_ui(self):
        """Triggers a GUI update."""
        self.draw_pegs()
        self.root.update_idletasks()  # Ensures immediate UI refresh



def play():
    game = Solitaire()
    while not game.is_game_over():
        game.display()
        try:
            print(game.get_all_moves())
            x1, y1, x2, y2 = map(int, input("Enter move (x1 y1 x2 y2): ").split())
            if not game.move(x1, y1, x2, y2):
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter four integers.")

    game.display()
    print("Game Over!")




if __name__ == "__main__":
    root = tk.Tk()
    game_gui = SolitaireGUI(root)
    button = tk.Button(root,
                       text="Restart",
                       command=game_gui.game_restart,
                       activebackground="blue",
                       activeforeground="white",
                       anchor="center",
                       bd=3,
                       bg="lightgray",
                       cursor="hand2",
                       disabledforeground="gray",
                       fg="black",
                       font=("Arial", 12),
                       height=2,
                       highlightbackground="black",
                       highlightcolor="green",
                       highlightthickness=2,
                       justify="center",
                       overrelief="raised",
                       padx=10,
                       pady=5,
                       width=15,
                       wraplength=100)

    button.pack(padx=20, pady=20)
    root.mainloop()
