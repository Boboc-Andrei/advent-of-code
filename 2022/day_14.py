import asyncio
import os
from dataclasses import dataclass

SAND = 'o'
EMPTY = '.'
OBSTACLE = '#'
ENDLESS_FLOW = '~'

@dataclass
class Vector2:
    row: int
    col: int

class SimulationContext:
    def __init__(self, grid_size: Vector2):
        self.grid_size: Vector2 = grid_size
        self.grid = [['.' for _ in range(grid_size.col)] for _ in range(grid_size.row)]
        self.sand_position = Vector2(0, 500)
        self.steps_simulated = 0
        self.finished = False
        self.window_size = Vector2(30,60)
        self.sand_simulated = 0
        self.endless_void_detected =  False
        self.precompute_simulation = False
        
    def serialize_grid(self, separator: str = '') -> str:
        return '\n'.join([separator.join(line) for line in self.grid])
    
    def serialize_grid_window(self) -> str:
        start_row = self.sand_position.row - self.window_size.row // 2
        end_row = start_row + self.window_size.row
        
        start_col = self.sand_position.col - self.window_size.col // 2
        end_col = start_col + self.window_size.col
        
        if(start_row < 0):
            start_row = 0
            end_row = self.window_size.row
        
        if(end_row > self.grid_size.row):
            start_row = self.grid_size.row - self.window_size.row
            end_row = self.grid_size.row
        
        if(start_col < 0):
            start_col = 0
            end_col = self.window_size.col

        if(end_col > self.grid_size.col):
            start_col = self.grid_size.col - self.window_size.col
            end_col = self.grid_size.col
        

        return '\n'.join([' '.join(line[start_col:end_col]) + f' {start_row + idx}' for idx, line in enumerate(self.grid[start_row:end_row])])

    def get_status(self, current_animation_step: int) -> str:
        s = f"""
Grid size {self.grid_size}
Performed {self.steps_simulated} steps
Simulated {self.sand_simulated} grains\n"""
        if(self.finished):
            s += "Simulation Done.\n"
            s += f"Animation progress : {current_animation_step / self.steps_simulated * 100:.2f}%"
        else:
            s += "Simulating..."
        return s

async def endless_void_simulation(simulation: SimulationContext, queue: asyncio.Queue):
    position = simulation.sand_position
    grid = simulation.grid
    while(not simulation.finished):
        simulation.steps_simulated += 1
        
        if(not simulation.precompute_simulation):
            await asyncio.sleep(0)
        
        if(simulation.endless_void_detected):
            await queue.put((simulation.serialize_grid_window(), simulation.steps_simulated))
            
        
        if(position.row == simulation.grid_size.row - 1):
            grid[position.row][position.col] = ENDLESS_FLOW
            if(simulation.endless_void_detected):
                simulation.finished = True
            else:
                simulation.endless_void_detected = True
                position.row = 0
                position.col = 500
                grid[position.row][position.col] = SAND if not simulation.endless_void_detected else ENDLESS_FLOW
        elif(grid[position.row + 1][position.col] in (EMPTY, ENDLESS_FLOW)):
            grid[position.row][position.col] = ENDLESS_FLOW
            position.row += 1
            grid[position.row][position.col] = SAND if not simulation.endless_void_detected else ENDLESS_FLOW
        elif(grid[position.row+1][position.col-1] in (EMPTY, ENDLESS_FLOW)):
            grid[position.row][position.col] = ENDLESS_FLOW
            position.row += 1
            position.col -= 1
            grid[position.row][position.col] = SAND if not simulation.endless_void_detected else ENDLESS_FLOW
        elif(grid[position.row+1][position.col+1] in (EMPTY, ENDLESS_FLOW)):
            grid[position.row][position.col] = ENDLESS_FLOW
            position.row += 1
            position.col += 1
            grid[position.row][position.col] = SAND if not simulation.endless_void_detected else ENDLESS_FLOW
        else:
            await queue.put((simulation.serialize_grid_window(), simulation.steps_simulated))
            simulation.sand_simulated += 1
            position.row = 0
            position.col = 500
            grid[position.row][position.col] = SAND if not simulation.endless_void_detected else ENDLESS_FLOW
    
    await queue.put((simulation.serialize_grid_window(), simulation.steps_simulated))

async def floor_simulation(simulation: SimulationContext, queue: asyncio.Queue) -> None:
    position = simulation.sand_position
    grid = simulation.grid
    while(not simulation.finished):
        simulation.steps_simulated += 1
        
        if(not simulation.precompute_simulation):
            await asyncio.sleep(0)

        if(grid[position.row + 1][position.col] in (EMPTY, ENDLESS_FLOW)):
            grid[position.row][position.col] = ENDLESS_FLOW
            position.row += 1
            grid[position.row][position.col] = SAND
        elif(grid[position.row+1][position.col-1] in (EMPTY, ENDLESS_FLOW)):
            grid[position.row][position.col] = ENDLESS_FLOW
            position.row += 1
            position.col -= 1
            grid[position.row][position.col] = SAND
        elif(grid[position.row+1][position.col+1] in (EMPTY, ENDLESS_FLOW)):
            grid[position.row][position.col] = ENDLESS_FLOW
            position.row += 1
            position.col += 1
            grid[position.row][position.col] = SAND
        else:
            await queue.put((simulation.serialize_grid_window(), simulation.steps_simulated))
            simulation.sand_simulated += 1
            
            if(position == Vector2(0, 500)):
                simulation.finished = True
            
            position.row = 0
            position.col = 500
            grid[position.row][position.col] = SAND
    
    await queue.put((simulation.serialize_grid_window(), simulation.steps_simulated))

async def consumer(context: SimulationContext, queue: asyncio.Queue) -> None:
    while not context.finished or not queue.empty():
        grid_state, current_animation_step = await queue.get()
        os.system("cls")
        print(grid_state)
        print(context.get_status(current_animation_step))
        await asyncio.sleep(0.005)
        queue.task_done()

def generate_obstacles(context: SimulationContext, obstacles: list[list[list[int]]]) -> None:
    print(context.grid_size)
    for line in obstacles:
        prev_col, prev_row = line[0]
        
        for col, row in line[1:]:
            if(row == prev_row):
                ascending = 1 if col > prev_col else -1
                for i in range(prev_col, col + ascending , ascending):
                    context.grid[row][i] = OBSTACLE
            else:
                ascending = 1 if row > prev_row else -1
                for i in range(prev_row, row + ascending, ascending):
                    context.grid[i][col] = OBSTACLE
            prev_row, prev_col = row, col
     
async def main():
    
    obstacles = []
    with open("input_14.txt", 'r') as f:
        for line in f:
            line = [[int(num) for num in segment.strip().split(',')] for segment in line.split('->')]
            obstacles.append(line)
            
    size = Vector2(0,0)
    for line in obstacles:
        for obstacle in line:
            size.row = max(size.row, obstacle[1])
            size.col = max(size.col, obstacle[0])
    size.row += 3
    size.col += 150
    
    queue = asyncio.Queue()
    simulation_grid = SimulationContext(grid_size=size)

    generate_obstacles(simulation_grid, obstacles)
    
    try:
        sim_type = int(input("Choose simulation type:\n0 - Botomless void [Default]\n1 - Endless floor\n>"))
        if(sim_type not in [0,1]):
            print("Invalid input. Using default option")
            sim_type = 0
            await asyncio.sleep(3)
    except ValueError:
        sim_type = 0
    
    if(sim_type == 0):
        producer_task = asyncio.create_task(endless_void_simulation(simulation_grid, queue))
    elif(sim_type == 1):
        for col in range(size.col):
            simulation_grid.grid[size.row-1][col] = OBSTACLE
        producer_task = asyncio.create_task(floor_simulation(simulation_grid, queue))
        
    
    consumer_task = asyncio.create_task(consumer(simulation_grid, queue))
    
    await producer_task
    await consumer_task
    await queue.join()
    consumer_task.cancel()
    
asyncio.run(main())
