from collections import deque
from typing import Callable
grid = []

class Cell:
    def __init__(self, row: int, col: int, height: str):
        self.row = row
        self.col = col
        self.neighbours = []
        self.height_letter = height

    def __repr__(self):
        return f"[({self.row}, {self.col}), {self.height_letter}]"
    
    @property
    def position(self) -> tuple[int, int]: return self.row, self.col
    @property
    def height(self) -> int: return ord(self.height_letter[0])
    @height.setter
    def height(self, value: str): self.height_letter = value
    @staticmethod
    def height_difference(cell_from: "Cell", cell_to: "Cell"):
        return cell_to.height - cell_from.height

with open("input_12.txt", 'r') as f:
    for row_idx, line in enumerate(f):
        row = []
        for col_idx, character in enumerate(line.strip()):
            cell = Cell(row_idx, col_idx, character)
            
            if(character == 'S'):
                cell.height_letter = 'a'
                start = cell
            if(character == 'E'):
                cell.height_letter = 'z'
                end = cell
            row.append(cell)
        grid.append(row)

def get_climbable_neighbours(grid: list[list[Cell]], cell: Cell, orthogonal: bool = True, climbable_neighbour_condition: Callable[[Cell, Cell], bool] = None) -> list[Cell]:
    row, col = cell.position
    rows, cols = len(grid), len(grid[0])
    neighbour_positions = [
        (row+1, col),
        (row-1, col),
        (row, col+1),
        (row, col-1)
    ]
    
    if(orthogonal == False):
        neighbour_positions.extend([
            (row+1, col+1),
            (row+1, col+-1),
            (row-1, col+1),
            (row-1, col-1),
        ])
    
    
    if climbable_neighbour_condition == None:
        climbable_neighbour_condition = lambda cell, neighbour: Cell.height_difference(cell, neighbour) <= 1
            
    return [grid[n_row][n_col] for n_row, n_col in neighbour_positions if 0 <= n_row < rows and 0 <= n_col < cols and climbable_neighbour_condition(cell, grid[n_row][n_col])]


def find_shortest_path(grid: list[list[Cell]], source: Cell, stop_condition: Callable[[Cell], bool], orthogonal: bool = True, climbable_neighbour_condition = None) -> list[Cell]:
    shortest_path_found = []
    
    visited = set([source])
    queue = deque([(source, [])])

    visited_count = 0
    
    while(queue):
        current_node, current_path = queue.popleft()
        
        current_path = current_path + [current_node]
        
        if(stop_condition(current_node)):
            return current_path
        
        for neighbour in get_climbable_neighbours(grid, current_node, orthogonal, climbable_neighbour_condition):
            if neighbour in visited:
                continue
            visited.add(neighbour)
            queue.append((neighbour, current_path))
    
    return shortest_path_found

def reached_peak(destination: Cell):
    def stop_condition(cell: Cell):
        return cell == destination
    return stop_condition

def reached_altitude(target_height: str):
    def stop_condition(cell: Cell):
        return cell.height_letter == target_height
    return stop_condition

def trace_path(grid: list[list[Cell]], path: list[Cell]):
    rows, cols = len(grid), len(grid[0])
    path_map = [['.' for c in range(cols)] for r in range(rows)]
    print(len(path))
    end = path[-1]
    
    for idx in range(len(path) - 1):
        node = path[idx]
        next = path[idx + 1]
        path_map[node.row][node.col] = node.height_letter
    path_map[end.row][end.col] = 'X'
    return path_map

def print_matrix(matrix: list[list[str]], separator:str = ' '):
    for line in matrix:
        print(separator.join(line))

shortest_path_from_start_to_end = find_shortest_path(grid, start,
                                                     stop_condition = lambda cell: cell == end,
                                                     orthogonal = False,
                                                     climbable_neighbour_condition = lambda cell, neighbour: Cell.height_difference(cell, neighbour) <= 1)
path_map_1 = trace_path(grid, shortest_path_from_start_to_end)
print_matrix(path_map_1)
print(f"Shortest path length from start to end: {len(shortest_path_from_start_to_end) - 1}")
    
print()
    
shortest_path_from_end_to_a = find_shortest_path(grid, end,
                                                  stop_condition = lambda cell: cell.height_letter == 'a',
                                                  orthogonal = False,
                                                  climbable_neighbour_condition = lambda cell, neighbour: Cell.height_difference(cell, neighbour) >= -1)[::-1]
path_map_2 = trace_path(grid, shortest_path_from_end_to_a)
print_matrix(path_map_2, separator = '')
print(f"Shortest path from end to height 'a': {len(shortest_path_from_end_to_a) - 1}")


with open('temp.txt', 'w') as f:
    f.write('\n'.join([''.join(line) for line in path_map_2]))
    
    
