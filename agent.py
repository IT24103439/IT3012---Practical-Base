import random
import random
from collections import deque
import heapq

# agent.py
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

# P02 - Step 1.2: The Simple Reflex Agent (Implementation & Failure) - IT24103439
class SimpleReflexAgent:
    """A Simple Reflex Agent that operates strictly on current percepts using Condition-Action rules."""

    def sense_and_act(self, percept: dict) -> str:
        if percept.get('food_here'):
            return 'Up' # There is no "suck" action, it automatically consumes the food - IT24103439
        elif percept.get('wall_ahead'):
            return 'Left'
        else:
            return 'Up'

# P02 - Step 1.3: The Model-Based Agent (Memory & State) - IT24103439
class ModelBasedAgent:
    """A Model-Based Agent that maintains an internal memory state, avoids visited cells, and queries memory to escape loops."""

    def __init__(self, width=12, height=12):
        self.width = width
        self.height = height
        self.visited_cells = set()
        self.x = 0
        self.y = 0
        self.facing = 'Up'
        self.last_action = None
        self.visited_cells.add((self.x, self.y))

    def sense_and_act(self, percept: dict) -> str:
        # 1. Transition & Sensor Model: update position based on last action taken
        if self.last_action:
            if self.last_action == 'Up':
                self.y += 1
            elif self.last_action == 'Down':
                self.y -= 1
            elif self.last_action == 'Left':
                self.x -= 1
            elif self.last_action == 'Right':
                self.x += 1
            
            self.visited_cells.add((self.x, self.y))
            self.facing = self.last_action

        wall_ahead = percept.get('wall_ahead', False)
        food_here = percept.get('food_here', False)

        left_turns = {'Up': 'Left', 'Left': 'Down', 'Down': 'Right', 'Right': 'Up'}
        right_turns = {'Up': 'Right', 'Right': 'Down', 'Down': 'Left', 'Left': 'Up'}

        left_dir = left_turns[self.facing]
        right_dir = right_turns[self.facing]

        # Calculate coordinates for the cell directly ahead
        ax, ay = self.x, self.y
        if self.facing == 'Up': ay += 1
        elif self.facing == 'Down': ay -= 1
        elif self.facing == 'Left': ax -= 1
        elif self.facing == 'Right': ax += 1

        ahead_out_of_bounds = not (0 <= ax < self.width and 0 <= ay < self.height)
        ahead_is_visited = (ax, ay) in self.visited_cells

        # Calculate coordinates for the cell to the left
        lx, ly = self.x, self.y
        if left_dir == 'Up': ly += 1
        elif left_dir == 'Down': ly -= 1
        elif left_dir == 'Left': lx -= 1
        elif left_dir == 'Right': lx += 1

        left_out_of_bounds = not (0 <= lx < self.width and 0 <= ly < self.height)
        left_is_visited = left_out_of_bounds or ((lx, ly) in self.visited_cells)

        # Condition-Action rules avoiding visited cells and walls:
        if food_here:
            action = self.facing
        elif wall_ahead or ahead_out_of_bounds or ahead_is_visited:
            if left_is_visited:
                action = right_dir  # If ahead and left are both visited/blocked, turn right
            else:
                action = left_dir   # If ahead is visited/wall but left is free, turn left
        else:
            action = self.facing    # Move forward if path ahead is clear and unvisited

        self.last_action = action
        return action


# P03 - Step 1.2: The Search Agent (BFS, DFS, UCS) - IT24103439
class SearchAgent:
    """A Goal-Based Planning Agent that uses BFS, DFS, or UCS to find a path to the nearest food pellet before taking any physical action."""

    # Helper function which returns valid (neighbour_position, action) pairs from a given position - IT24103439
    def _get_neighbours(self, pos, walls, grid_size):
        x, y = pos
        width, height = grid_size
        neighbours = []
        for action, (dx, dy) in [('Up', (0, 1)), ('Down', (0, -1)), ('Left', (-1, 0)), ('Right', (1, 0))]:
            nx, ny = x + dx, y + dy
            # Only add if within grid bounds and not a wall - IT24103439
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
                neighbours.append(((nx, ny), action))
        return neighbours

    # BFS: explores shallowest nodes first - IT24103439
    def bfs_search(self, start, goal, walls, grid_size):
        frontier = deque()
        frontier.append((start, []))
        reached = set() # Graph search: prevents revisiting nodes - IT24103439
        reached.add(start)

        while frontier:
            current_pos, path = frontier.popleft()  # FIFO: pop from left - IT24103439
            if current_pos == goal:
                return path
            for next_pos, action in self._get_neighbours(current_pos, walls, grid_size):
                if next_pos not in reached:
                    reached.add(next_pos)
                    frontier.append((next_pos, path + [action]))
        return []

    # DFS: explores deepest nodes first - IT24103439
    def dfs_search(self, start, goal, walls, grid_size):
        frontier = []
        frontier.append((start, []))
        reached = set() # Graph search - IT24103439
        reached.add(start)

        while frontier:
            current_pos, path = frontier.pop()  # LIFO: pop from right - IT24103439
            if current_pos == goal:
                return path
            for next_pos, action in self._get_neighbours(current_pos, walls, grid_size):
                if next_pos not in reached:
                    reached.add(next_pos)
                    frontier.append((next_pos, path + [action]))
        return []

    # UCS: orders by total path cost g(n) - IT24103439
    def ucs_search(self, start, goal, walls, grid_size):
        frontier = []
        heapq.heappush(frontier, (0, start, []))
        reached = set() # Graph search - IT24103439

        while frontier:
            cost, current_pos, path = heapq.heappop(frontier)   # Pop lowest cost - IT24103439
            if current_pos in reached:
                continue
            reached.add(current_pos)
            if current_pos == goal:
                return path
            for next_pos, action in self._get_neighbours(current_pos, walls, grid_size):
                if next_pos not in reached:
                    heapq.heappush(frontier, (cost + 1, next_pos, path + [action]))
        return []

    # P03 - Step 1.3: Executing and Comparing Offline Plans
    def __init__(self):
        self.plan = []  # Stores the sequence of actions to execute - IT24103439
        self.active_algo = 'BFS'    # Switch algorithms - IT24103439

    # If plan is empty, run the chosen search to refill it
    def sense_and_act(self, percept: dict) -> str:
        agent_pos = tuple(percept['agent_pos'])
        all_food  = percept['all_food']
        walls     = set(map(tuple, percept['walls']))
        grid_size = percept['grid_size']

        if not self.plan:
            if not all_food:
                return 'Up' # No food left, fallback action - IT24103439
            closest_food = min(all_food, key=lambda f: abs(f[0] - agent_pos[0]) + abs(f[1] - agent_pos[1])) # Find closest food using Manhattan distance - IT24103439

            # Run the selected search algorithm - IT24103439
            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(agent_pos, tuple(closest_food), walls, grid_size)
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(agent_pos, tuple(closest_food), walls, grid_size)
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(agent_pos, tuple(closest_food), walls, grid_size)

        # Execute next action from the front of the plan - IT24103439
        if self.plan:
            return self.plan.pop(0)

        return 'Up'   # Safety fallback if search returned empty path - IT24103439