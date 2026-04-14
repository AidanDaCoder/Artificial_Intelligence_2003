import heapq

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


def step_cost(grid, current, successor):
    current_row, current_col = current
    successor_row, successor_col = successor

    current_height = grid[current_row][current_col]
    successor_height = grid[successor_row][successor_col]

    return 1 + max(0, successor_height - current_height)

def ucs(grid, start, goal):
    pq = []
    visited = set()
    best_cost = {}

    start_node = {
        "state": start,
        "parent": None,
        "g": 0
    }

    heapq.heappush(pq, (0, start, start_node))
    best_cost[start] = 0

    while pq:
        current_cost, current_state, current_node = heapq.heappop(pq)
        
        if current_state in visited:
            continue

        if current_state == goal:
            return current_node

        visited.add(current_state)

        for successor in get_successors(current_state, grid):
            new_cost = current_node["g"] + step_cost(grid, current_state, successor)
            
            if successor not in best_cost or new_cost < best_cost[successor]:
                best_cost[successor] = new_cost
                child_node = {
                    "state": successor,
                    "parent": current_node,
                    "g": new_cost
                }

                heapq.heappush(pq, (new_cost, successor, child_node))
        
    return None


if __name__ == "__main__":
    import sys

    mode = sys.argv[1]
    map_file = sys.argv[2]
    algorithm = sys.argv[3]
    # heuristic = sys.argv[4]

    rows, cols, start, goal, grid = parse_map(map_file)
    
    goal_node = None

    if algorithm == "bfs":
        goal_node = bfs(grid, start, goal)
    elif algorithm == "ucs":
        goal_node = ucs(grid, start, goal)
    else:
        goal_node = None
    
    if goal_node is None:
        print("null")
    else:
        path = make_path(goal_node)
        print_path(grid, path)








