def grid_reconstruction(lines):
    def max_len(li):
        result = 0
        for l in li:
            if len(l) > result:
                result = len(l)
        return result

    '''
    This function serve to know if an element are already present in the grid.
    It will return the coordonates in the grid and the coordonate of the first element of the line found in the grid
    Input : gr => the grid
    Ouput : inside (bool), coordonates (array) 
    '''
    def get_pos(gr, li):
        for x in range(len(gr)):
            for y in range(len(gr)):
                for i in range(len(li)):
                    if is_equals(grid[y][x],li[i]):
                        return True, [x,y,i]
        return False, []
    
    def empty_row(row):
        for x in row:
            if not is_empty(x):
                return False
        return True
    
    def move_line_grid(grid,grid_filled, index_start, index_stop, row):
        remplaced_line = []
        if row:
            for pos, val in enumerate(grid[index_start]):
                temp = grid[index_stop][pos]
                if not is_empty(temp):
                    remplaced_line.append(temp)
                grid[index_stop][pos] = val
                grid[index_start][pos] = emptyness
            grid_filled[0].discard(index_start)
            grid_filled[0].add(index_stop)
        else:
            for val in grid:
                temp = val[index_stop]
                if not is_empty(temp):
                    remplaced_line.append(temp)
                val[index_stop] = val[index_start]
                val[index_start] = emptyness
            grid_filled[1].discard(index_start)
            grid_filled[1].add(index_stop)
        return remplaced_line


    def fill_grid(grid, grid_filled, line, pos_g, pos_l, horizontal):
        new_pos_g = pos_g
        returned_lines = []
        if horizontal:
            if pos_g[0] < pos_l:  # TODO a modifier pour les ligne incomplete
                returned_lines.append(move_line_grid(grid, grid_filled, pos_g[0], pos_l, False))
                new_pos_g[0] = pos_l
        else:
            if pos_g[1] < pos_l:
                returned_lines.append(move_line_grid(grid, grid_filled, pos_g[1], pos_l, True))
                new_pos_g[1] = pos_l
                
        for pos, val in enumerate(line):
            if horizontal:
                pos_grid = [pos -pos_l + new_pos_g[0] ,new_pos_g[1]]
            else:
                pos_grid = [new_pos_g[0], pos -pos_l + new_pos_g[1]]
                
            if not is_equals(grid[pos_grid[1]][pos_grid[0]], val) and not is_empty(grid[pos_grid[1]][pos_grid[0]]):
                if horizontal:
                    returned_lines.append(empty_line(grid, grid_filled, pos_grid[0], False ))
                else:
                    returned_lines.append(empty_line(grid, grid_filled, pos_grid[1], True ))
            grid[pos_grid[1]][pos_grid[0]] = val
        return returned_lines
        
    def is_empty(val):
        return val == emptyness
    def is_equals(val1, val2):
        return val1 == val2
    
    def empty_line(grid, grid_filled, index, is_row):
        returned_line = []
        if is_row:
            grid_filled[0].discard(index)
            for p, val in grid[index]:
                if not is_empty(val):
                    returned_line.append(val)
                    grid[index][p] = empty
        else:
            grid_filled[1].discard(index)
            for p, val in enumerate(grid):
                if not is_empty(val[index]):
                    returned_line.append(val)
                    grid[p][index] = empty
        return returned_line
            
                    
        
                
    emptyness = [-1]
    maxleng= max_len(lines)
    grid = [[emptyness for _ in range(maxleng)] for _ in range(maxleng)]
    grid_filled = [set({}),set({})] # row and then col
    ret_lines = []
    empty_place_start= [0,0] # TODO to change ugly
    
    for line in lines:

        inside, pos = get_pos(grid, line)
        if not inside:
            rettt = fill_grid(grid, grid_filled, line, empty_place_start , 0, True)
            grid_filled[0].add(empty_place_start[1])
            empty_place_start[1] += 1
            ret_lines.append(rettt)
        else:
            if not pos[1] in grid_filled[0]:
                rettt = fill_grid(grid, grid_filled, line, pos[0:2], pos[2], True)
                grid_filled[0].add(pos[1])
                for ret in rettt:
                    lines.append(ret)
            else:
                rettt = fill_grid(grid, grid_filled, line, pos[0:2], pos[2], False)
                grid_filled[1].add(pos[0])
                for ret in rettt:
                    lines.append(ret)
    for ll in grid:
        print(ll)
    return 
"""
lines_exemple = [[[0,0],[0,1],[0,2]]
                 ,[[1,0],[1,1],[1,2]]
                 ,[[0,1],[1,1],[2,1]]
                 ,[[2,0],[2,1],[2,2]]
                 ,[[0,2],[1,2],[2,2]]]
grid_reconstruction(lines_exemple)
"""
lines_exemple2 = [[[1,0],[1,1],[1,2]]
                 ,[[0,0],[0,1],[0,2]]
                 ,[[0,1],[1,1],[2,1]]
                 ,[[2,0],[2,1],[2,2]]
                 ,[[0,2],[1,2],[2,2]]]
grid_reconstruction(lines_exemple2)

        