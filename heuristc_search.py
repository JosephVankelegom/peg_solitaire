import time
from copy import deepcopy
import peg_solitaire as ps

def play_turn(ia, game, game_ui, root):
    if game.is_game_over():
        print("Game Over!")
        return

    try:
        x1, y1, x2, y2 = ia.get_move(game)
        if game.move(x1, y1, x2, y2):
            print("move:", x1, y1, "->", x2, y2)
            game_ui.update_ui()  # Update the GUI
            root.after(500, lambda: play_turn(ia, game, game_ui, root))  # Schedule next move
        else:
            print("Invalid move.")
    except ValueError:
        print("Invalid input. Please enter four integers.")


class MinMax_Solo:
    def __init__(self, depth, eval_fun):
        self.depth = depth
        self.eval_fun = eval_fun
    def get_move(self, node):
        all_moves = {}
        result = ()
        best_value = float("-inf")
        for move in node.get_all_moves():
            next_node = node.successor(move)
            value = heuristc_search(next_node, self.depth - 1, self.eval_fun)
            all_moves[move] = value
            if best_value < value : result = move
        return result




###########
#  Search #
###########


def heuristc_search(node, depth, eval_fun):
    all_moves = node.get_all_moves()
    if depth == 0 or len(all_moves) == 0:
        return eval_fun(node)
    value = float("-inf")
    for move in all_moves:
        next_node = node.successor(move)
        value = max(value, heuristc_search(next_node, depth - 1, eval_fun))
    return value


###########
#  Eval   #
###########
def number_of_moves(node):
    return len(node.get_all_moves())


#test1
if __name__ == "__main__":
    root = ps.tk.Tk()
    game_gui = ps.SolitaireGUI(root)
    ia = MinMax_Solo(5, number_of_moves)
    play_turn(ia, ps.Solitaire(), game_gui, root)
    root.mainloop()
