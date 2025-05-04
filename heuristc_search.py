import time
from copy import deepcopy
import peg_solitaire as ps

def play_turn_ui(ia, game, game_ui, root):
    while not game.is_game_over():
        try:
            x1, y1, x2, y2 = ia.get_move(game)
            if game.move((x1, y1, x2, y2)):
                game_ui.move(x1, y1)  # Update the GUI
                root.update()
                time.sleep(0.5)
                game_ui.move(x2, y2)
                root.update()
            else:
                print("Invalid move.")
        except ValueError:
            print("Invalid input. Please enter four integers.")
    print("game Over")


def play(ia, game, args):
    return ia(game, args)


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
            if best_value < value :
                result = move
                best_value = value
        return result


#test1





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


def Depth_First_Search(node_o, args_dfs):
    if len(args_dfs) != 5 :
        "wrong number of args, should be: result, eval_function, args_eval, stop_function, args_stop"
        return []
    result, eval_function, args_eval, stop_function, args_stop = args_dfs
    @count_explored  # Application du décorateur
    def Depth_First_Search_int(node, path, bests_paths, eval_fun, stop_fun):
        all_moves = node.get_all_moves()
        if len(all_moves) == 0:
            val = eval_fun(node, args_eval)
            if val == 100:
                bests_paths.extend([path])
            return
        for move in all_moves:
            if stop_fun(node, args_stop):
                return
            new_path = deepcopy(path)
            new_path.append(move)
            Depth_First_Search_int(node.successor(move), new_path, bests_paths, eval_fun, stop_fun)
        return
    Depth_First_Search_int(node_o, [], result, eval_function, stop_function)
    print("Nombre de nœuds explorés DFS:", Depth_First_Search_int.counter)
    return result


def Breadth_First_Search(node_o, args_bfs):
    if len(args_bfs) != 6 :
        "wrong number of args, should be: result, eval_function, args_eval, stop_function, args_stop"
        return []
    result, all_nodes, eval_function, args_eval, stop_function, args_stop = args_bfs

    @count_explored  # Application du décorateur
    def Breadth_First_Search_int(node, all_n, path, bests_paths, eval_fun, stop_fun):
        if stop_fun(node, args_stop):
            return
        all_moves = node.get_all_moves()
        if len(all_moves) == 0:
            val = eval_fun(node, args_eval)
            if val == 100:
                bests_paths.extend([path])
            return
        for move in all_moves:
            new_path = deepcopy(path)
            new_path.append(move)
            all_n.append(node.successor(move))
        Breadth_First_Search_int(all_n.pop(0), new_path, bests_paths, eval_fun, stop_fun)
        return
    Breadth_First_Search_int(node_o, all_nodes, [], result, eval_function, stop_function)
    print("Nombre de nœuds explorés DFS:", Breadth_First_Search_int.counter)
    return result

class PreprocessPath:

    def __init__(self, pathway):
        self.path = pathway
    def get_move(self, node):
        return self.path.pop(0)




###########
#  Eval   #
###########
def number_of_moves(node, args_eval):
    return len(node.get_all_moves())

def pieces_center(node):
    pegs = 0
    pegs_c = 0
    pegs_t = 0
    def touching(x, y):
        for x_t in [x-1,x,x+1]:
            for y_t in [y-1,y,y+1]:
                if (x_t != x or y_t != y) and (0<=x_t<=6 and 0<=y_t<=6) and node.board[y_t, x_t] == 1:
                    return True
        return False

    for y in range(7):
        for x in range(7):
            if node.board[y, x] == 1:
                pegs += 1
                if touching(x,y):
                    pegs_t += 1
                if 2<= x <= 4 and 2 <= y <= 4:
                    pegs_c += 1

    result = 500 + pegs_c + pegs_t + len(node.get_all_moves()) - (pegs * 10)
    if pegs == 1:
        result = float("inf")
    return result

def stop_of_pieces(node, args):
    bests_path, depth = args
    return len(bests_path) == depth

def number_of_pieces(node, args_eval):
    return 101 - node.number_of_pegs



#################
#   Stats       #
#################

def count_explored(func):
    def wrapper(*args, **kwargs):
        wrapper.counter += 1
        return func(*args, **kwargs)
    wrapper.counter = 0
    return wrapper





if __name__ == "__uirun__":
    root = ps.tk.Tk()
    game_gui = ps.SolitaireGUI(root)
    ia = MinMax_Solo(5, pieces_center)
    play_turn_ui(ia, ps.Solitaire(), game_gui, root)


if __name__ == "__main__":
    ui = True
    paths = []
    game = ps.Solitaire()
    all_nodes = [game]
    args = (paths, number_of_pieces, (), stop_of_pieces, (paths, 100))
    play(Depth_First_Search, game, args)
    print(paths)

    if ui :
        for path in paths:
            root = ps.tk.Tk()
            game_gui = ps.SolitaireGUI(root)
            ia = PreprocessPath(path)
            play_turn_ui(ia, ps.Solitaire(), game_gui, root)
        root.mainloop()

