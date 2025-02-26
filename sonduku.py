import copy
import time


class Problem(object):

    def __init__(self, initial):
        self.initial = initial
        self.size = len(initial) # Size of grid
        self.height = int(self.size/3) # Size of a quadrant

    def check_legal(self, state):
        # Expected sum of each row, column or quadrant.
        total = sum(range(1, self.size+1))

        # Check rows and columns and return false if total is invalid
        for row in range(self.size):
            if (len(state[row]) != self.size) or (sum(state[row]) != total):
                return False

            column_total = 0
            for column in range(self.size):
                column_total += state[column][row]

            if (column_total != total):
                return False

        # Check quadrants and return false if total is invalid
        for column in range(0,self.size,3):
            for row in range(0,self.size,self.height):

                block_total = 0
                for block_row in range(0,self.height):
                    for block_column in range(0,3):
                        block_total += state[row + block_row][column + block_column]

                if (block_total != total):
                    return False

        return True

    # Return set of valid numbers from values that do not appear in used
    def filter_values(self, values, used):
        return [number for number in values if number not in used]

    # Return first empty spot on grid (marked with 0)
    def get_spot(self, board, state):
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column

    # Filter valid values based on row
    def filter_row(self, state, row):
        number_set = range(1, self.size+1) # Defines set of valid numbers that can be placed on board
        in_row = [number for number in state[row] if (number != 0)]
        options = self.filter_values(number_set, in_row)
        return options

    # Filter valid values based on column
    def filter_col(self, options, state, column):
        in_column = []
        for column_index in range(self.size):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.filter_values(options, in_column)
        return options

    # Filter valid values based on quadrant
    def filter_quad(self, options, state, row, column):
        in_block = [] # List of valid values in spot's quadrant
        row_start = int(row/self.height)*self.height
        column_start = int(column/3)*3
        
        for block_row in range(0, self.height):
            for block_column in range(0,3):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.filter_values(options, in_block)
        return options    

    def actions(self, state):
        row,column = self.get_spot(self.size, state) # Get first empty spot on board

        # Remove a square's invalid values
        options = self.filter_row(state, row)
        options = self.filter_col(options, state, column)
        options = self.filter_quad(options, state, row, column)

        # Return a state for each valid option (yields multiple states)
        for number in options:
            new_state = copy.deepcopy(state) # Norvig used only shallow copy to copy states; deepcopy works like a perfect clone of the original
            new_state[row][column] = number
            yield new_state

class Node:

    def __init__(self, state):
        self.state = state

    def expand(self, problem):
        # Return list of valid states
        return [Node(state) for state in problem.actions(self.state)]

def DFS(problem):
    start = Node(problem.initial)
    if problem.check_legal(start.state):
        return start.state

    stack = []
    stack.append(start) # Place initial node onto the stack
    x = 1

    while stack: 
        node = stack.pop() # Pops the last node, tests legality, then expands the same popped node
        if problem.check_legal(node.state):
            return node.state
        print(x)
        x+=1
        for row in node.state:
            print(row)
            
            
        stack.extend(node.expand(problem)) # Add viable states onto the stack...
        # ...by using expand method of Node class, taking in problem parameter of this function to
        # ...make use of actions method of the Problem class, yielding new possible states from the 
        # ...Node popped. Then the cycle repeats until complete.

    return None

def DFS_solve(board):
    print ("\nSolving with DFS...")

    start_time = time.time()
    problem = Problem(board)
    solution = DFS(problem)
    elapsed_time = time.time() - start_time
          
    if solution:
        print ("Found solution")
        for row in solution:
            print (row)
    else:
        print ("No possible solutions")

    print ("Elapsed time: " + str(elapsed_time) + " seconds")




if __name__ == "__main__":
    print ("\n\nTesting on invalid 9x9 grid...")
    grid =[[0,0,7,2,8,0,0,0,0], 
      [0,0,0,0,0,0,5,0,6],
      [4,1,3,0,0,6,0,8,0],
      [7,2,0,3,9,0,0,0,0],
      [3,4,0,0,0,0,8,1,0],
      [6,8,0,1,0,7,0,0,2],
      [0,0,0,6,7,4,0,2,3],
      [0,0,0,0,0,5,7,0,0],
      [1,0,6,0,2,3,0,4,0]]


    print ("Problem:")
    for row in grid:
        print (row)
    DFS_solve(grid)

