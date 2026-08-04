import random

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