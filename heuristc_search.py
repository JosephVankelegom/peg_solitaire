from copy import deepcopy
from peg_solitaire import Solitaire

def play():
    game = Solitaire()
    while not game.is_game_over():
        game.display()
        try:
            x1, y1, x2, y2 = get_move(game, 3, number_of_moves)
            if not game.move(x1, y1, x2, y2):
                print("Invalid move.")
                break
            print("move : ", x1," ", y1, " ", x2, " ", y2)
        except ValueError:
            print("Invalid input. Please enter four integers.")
            print(game.get_all_moves())
            print(get_move(game, 3, number_of_moves))
            break

    game.display()
    print("Game Over!")


def get_move(node, depth, eval):
    all_moves = {}
    result = ()
    best_value = float("-inf")
    for move in node.get_all_moves():
        next_node = deepcopy(node)
        next_node.move(*move)
        value = heuristc_search(next_node, depth - 1, eval)
        all_moves[move] = value
        if best_value < value : result = move
    return result




###########
#  Search #
###########


def heuristc_search(node: Solitaire, depth, eval):
    all_moves = node.get_all_moves()
    if depth == 0 or len(all_moves) == 0:
        return eval(node)
    value = float("-inf")
    for move in all_moves:
        next_node = deepcopy(node)
        next_node.move(*move)
        value = max(value, heuristc_search(next_node, depth-1, eval))
    return value


###########
#  Eval   #
###########
def number_of_moves(node):
    return len(node.get_all_moves())


#test
if __name__ == "__main__":
    play()