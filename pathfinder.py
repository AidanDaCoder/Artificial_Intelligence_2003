

def parse_map(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    #clean lines (removes \n and extra spaces)
    lines = [line.strip() for line in lines]

    #first line of rows and cols
    rows, cols = map(int, lines[0].split())

    #second line start position converting to 0-index for Python indexing
    row_start, col_start = map(int, lines[1].split())
    start = (row_start - 1, col_start - 1)

    #third line goal position same conversion as above
    row_goal, col_goal = map(int, lines[2].split())
    goal = (row_goal - 1, col_goal - 1)
    
    #main grid
    grid = []
    for i in range(3, 3 + rows):
        row = []
        for coordinate in lines[i].split():
            if coordinate == 'X':
                row.append('X')
            else:
                row.append(int(coordinate))
        grid.append(row)
    
    return rows, cols, start, goal, grid


def get_successors(state, grid):
    row, col = state
    successors = []

    #up, down, left, right
    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    rows = len(grid)
    cols = len(grid[0])

    for row_direction, col_direction in directions:
        new_row = row + row_direction
        new_col = col + col_direction

        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] != 'X':
                successors.append((new_row, new_col))
        
    
    return successors

def bfs(grid, start, goal):
    queue = []
    visited = set()

    start_node = {
        "state": start,
        "parent": None
    }

    queue.append(start_node)

    while queue:
        current_node = queue.pop(0)
        current_state = current_node["state"]
        
        if current_state not in visited:
            if current_state == goal:
                return current_node
            
            visited.add(current_state)

            for successor in get_successors(current_state, grid):
                if successor not in visited:
                    child_node = {
                        "state": successor,
                        "parent": current_node
                    }
                    queue.append(child_node)
                    
    return None

def make_path(goal_node):
    path = []
    current = goal_node
    
    while current is not None:
        path.append(current["state"])
        current = current["parent"]
    
    path.reverse()
    return path

def print_path(grid, path):
    temp_grid = []

    for row in grid:
        temp_grid.append(row.copy())

    for r, c in path:
        temp_grid[r][c] = "*"

    for row in temp_grid:
        print(" ".join(str(cell) for cell in row))

if __name__ == "__main__":
    import sys

    mode = sys.argv[1]
    map_file = sys.argv[2]
    algorithm = sys.argv[3]
    heuristic = sys.argv[4]

    rows, cols, start, goal, grid = parse_map(map_file)
    
    goal_node = None

    if algorithm == "bfs":
        goal_node = bfs(grid, start, goal)
    else:
        goal_node = None
    
    if goal_node is None:
        print("null")
    else:
        path = make_path(goal_node)
        print_path(grid, path)








