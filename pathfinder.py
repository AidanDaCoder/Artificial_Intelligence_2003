import heapq
import math

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
    #gets coordinates
    current_row, current_col = current
    successor_row, successor_col = successor

    #gets elevation values
    current_height = grid[current_row][current_col]
    successor_height = grid[successor_row][successor_col]

    return 1 + max(0, successor_height - current_height)

def ucs(grid, start, goal):
    pq = [] #priority queue 
    #visited = set()
    best_cost = {}
    insertion_order = 0

    start_node = {
        "state": start,
        "parent": None,
        "path_cost": 0
    }

    #add start node to heap and set start cost to 0
    heapq.heappush(pq, (0, insertion_order, start_node))
    best_cost[start] = 0

    while pq:
        current_cost, _, current_node = heapq.heappop(pq) #removes lowest cost node
        current_state = current_node["state"]

        if current_cost > best_cost[current_state]:
            continue

        #skip if node is already visited
        # if current_state in visited:
        #     continue

        if current_state == goal:
            return current_node

        # visited.add(current_state)

        for successor in get_successors(current_state, grid):
            new_cost = current_node["path_cost"] + step_cost(grid, current_state, successor)
            
            if successor not in best_cost or new_cost < best_cost[successor]:
                best_cost[successor] = new_cost
                child_node = {
                    "state": successor,
                    "parent": current_node,
                    "path_cost": new_cost
                }

                heapq.heappush(pq, (new_cost, insertion_order, child_node))
                insertion_order += 1

    return None

def euclidean(current, goal):
    x1, y1 = current
    x2, y2 = goal
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def manhattan(current, goal):
    x1, y1 = current
    x2, y2 = goal
    return abs(x2 - x1) + abs(y2 - y1)

def astar(grid, start, goal, heuristic_str):
    pq = [] #priority queue
    best_cost = {}
    insertion_order = 0

    if heuristic_str == "manhattan":
        heuristic = manhattan
    elif heuristic_str == "euclidean":
        heuristic = euclidean
    else:
        return None
    
    start_node = {
        "state": start,
        "parent": None,
        "path_cost": 0
    }

    start_priority = heuristic(start, goal)

    #push starting node into pq
    heapq.heappush(pq, (start_priority, insertion_order, start_node))
    best_cost[start] = 0
    insertion_order += 1

    while pq:
        current_priority, _, current_node = heapq.heappop(pq)
        current_state = current_node["state"]

        if current_node["path_cost"] > best_cost[current_state]:
            continue

        if current_state == goal:
            return current_node
        
        #loop works by exploring nodes in order of lowest total cost
        for successor in get_successors(current_state, grid):
            new_cost = current_node["path_cost"] + step_cost(grid, current_state, successor)

            if successor not in best_cost or new_cost < best_cost[successor]:
                best_cost[successor] = new_cost

                child_node = {
                    "state": successor,
                    "parent": current_node,
                    "path_cost": new_cost
                }

                total_cost = new_cost + heuristic(successor, goal)

                #push into pq using insertion_order
                heapq.heappush(pq, (total_cost, insertion_order, child_node))
                insertion_order += 1

    return None



if __name__ == "__main__":
    import sys

    mode = sys.argv[1]
    map_file = sys.argv[2]
    algorithm = sys.argv[3]
    heuristic = sys.argv[4] if len(sys.argv) > 4 else None #cos gradescope breaks

    rows, cols, start, goal, grid = parse_map(map_file)
    
    goal_node = None

    if algorithm == "bfs":
        goal_node = bfs(grid, start, goal)
    elif algorithm == "ucs":
        goal_node = ucs(grid, start, goal)
    elif algorithm == "astar":
        goal_node = astar(grid, start, goal, heuristic)
    else:
        goal_node = None
    
    if goal_node is None:
        print("null")
    else:
        path = make_path(goal_node)
        print_path(grid, path)


