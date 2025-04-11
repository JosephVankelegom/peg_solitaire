def grid_reconstruction(lines):
    empty = -1
    def max_len(li):
        result = 0
        for l in li:
            if len(l) > result:
                result = len(l)
        return result
    
    def get_pos(gr, li):
        for x in range(grid):
            if inside: break
            for y in range(grid):
                if inside: break
                for i in range(line):
                    if inside: break
                    if np.array_equals(grid[y][x],line[i]):
                        return True, [x,y,i]
        return False, []
    
    def empty_row(row):
        for x in row:
            if not np.array_equals(x,np.array([-1])):
                return False
        return True
    
    def move_line_grid(grid,grid_filled, index_start, index_stop, row):
        remplaced_line = []
        if row:
            for pos, val in enumerate(grid[index_start]):
                temp = grid[index_stop][pos]
                remplaced_line.append(temp)
                grid[index_stop][pos] = val
                grid[index_start][pos] = empty
            grid_filled[0].discard(index_start)
            grid_filled[0].add(index_stop)
        else:
            for val in grid:
                temp = val[index_stop]
                remplaced_line.append(temp)
                val[index_stop] = val[index_start]
                val[index_start] = empty
            grid_filled[1].discard(index_start)
            grid_filled[1].add(index_stop)
        return remplaced_line

    
    def fill_grid(grid, grid_filled, line, pos_g, pos_l, horizontal):
        new_pos_g = pos_g
        returned_line = []
        if horizontal:
            if pos_g[0] < pos_l:
                move_line_grid(grid, grid_filled, posg[0], pos_l, False)
                new_pos_g[0] = pos_l
        else:
            if pos_g[1] < pos_l:
                move_line_grid(grid, posg[1], pos_l, True)
                new_pos_g[1] = pos_l
                
        for pos, val in enumerate(line):
            if horizontal:
                pos_grid = [new_pos_g[0] ,pos_cal + new_pos_g[1]]
            else:
                pos_grid = [pos_cal + new_pos_g[0], new_pos_g[1]]
                
            if not is_empty(grid[new_pos_g[0], new_pos_g[1]]):
                if horizontal:
                    returned_line.append(empty_line(grid, grid_filled, grid[new_pos_g[0]], False ))
                else:
                    returned_line.append(empty_line(grid, grid_filled, grid[new_pos_g[1]], True ))
            grid[new_pos_g[0], new_pos_g[1]] = val
        return returned_line
        
    def is_empty(val):
        return val == empty
    
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
    grid_filled = [{},{}] # row and then col
    ret_lines = []
    
    for line in lines:
        inside, pos = get_pos(grid, line)
        if not inside:
            rettt = fill_grid(grid, grid_filled, line, [0,0], 0, True)
            ret_lines.append(rettt)
        else:
            if pos[1] in grid_filled[0]:
                rettt = fill_grid(grid, grid_filled, line, pos[0:2], pos[2], False)
                ret_lines.append(rettt)
            else:
                rettt = fill_grid(grid, grid_filled, line, pos[0:2], pos[2], True)
                ret_lines.append(rettt)
    for ll in grid:
        print(ll)
    return 

lines_exemple = [[[0,0],[0,1],[0,2]]
                 ,[[1,0],[1,1],[1,2]]
                 ,[[2,0],[2,1],[2,2]]
                 ,[[3,0],[3,1],[3,2]]
                 ,[[1,1],[2,1],[3,1]]]
grid_reconstruction(lines_exemple)


        