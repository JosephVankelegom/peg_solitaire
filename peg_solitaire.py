import numpy as np


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
    play()