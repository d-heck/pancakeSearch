## @ Author: David Heck (dheck@udel.edu)
#  This code demonstrates several algorithms to solve the Pancake Sorting Problem.

import copy # Used for deep copy
import re # for checking input

## Queue Structure (Stack of Pancakes and functions)
class PancakeQueue(object):
    def __init__(self): 
        self.queue = []
        self.goalFlag = 0 # Used to escape recursion in DFS
  
    def __str__(self): 
        return ' '.join([str(i) for i in self.queue]) 
  
    # for checking if the queue is empty 
    def isEmpty(self): 
        return len(self.queue) == [] 
  
    # for inserting an element in the queue 
    def push(self, data): 
        self.queue.append(data)

    # for deleting an element based on Priority 
    def delete(self): 
        try: 
            max = 0
            for i in range(len(self.queue)): 
                if self.queue[i] > self.queue[max]: 
                    max = i 
            item = self.queue[max] 
            del self.queue[max] 
            return item 
        except IndexError: 
            print() 
            exit()
    
    # Returns the cost of flipping from one state to the next
    def getCost(self, nextState):
        for i in range(3):
            if self.queue[i] != nextState[i]:
                return (4 - i)
        return 0
                
    # Returns the heuristic of a pancake
    def getHeuristic(self):
        if self.queue[0] != "4":
            return "4"
        if self.queue[1] != "3":
            return "3"
        if self.queue[2] != "2":
            return "2"
        if self.queue[3] != "1":
            return "1"
        return "0"
    
    # Checks if the current state is a goal state
    def goalTest(self):
        if (self.queue[0] == "4" and self.queue[1] == "3" and self.queue[2] == "2" and self.queue[3] == "1"): 
            return True
        return False

    # Flip pancake stack from specific point
    def flip(self, data):
        # Variables and Objects
        snapshot = self.queue[:] # Shallow copy so queue isn't modified.
        tempQueue = [] # Temporary queue for rebuilding the stack    
        pancake = self.queue[data] # Set marker for the value at position [data]

        # Pop all pancakes to the right of the pancake at position [data] then pop that pancake too
        while pancake in snapshot:
            tempQueue.append(snapshot.pop())

        # Rebuild queue (flipped from position [data])
        for pancake in tempQueue:
            snapshot.append(pancake)
        
        # Return flipped stack
        return snapshot

    # Helper function, returns formatted output (visualization) for what flip just took place and for what costs
    def printFlip(self,data,cost,heuristic):
        builder = ''
        for i in range(4):
            if i == data:
                builder += "|"
            builder += self.queue[i]
        builder += (" g=" + str(cost) + ", " + "h=" + str(heuristic))
        return builder

    # Takes the current state and lists the potential next states
    def generateChildrenStates(self):
        stateA = self.flip(0)
        stateB = self.flip(1)
        stateC = self.flip(2)
        return [stateA, stateB, stateC]


## Helper Functions
# Prints all of the flips, cost, and heuristic values of a specific path taken to get to a goal state
def printPath(path):
    # Get length of path
    n = len(path)
    output = []
    cost = 0

    # Build Output For Each Flip
    for i in range(n - 1):
        # Reinit Variables
        builder = ""
        flipFlag = 0
        heuristic = "0"
        currCost = 0

        # Build string representation of flip eg "12|24 g=3, h=0"
        for j in range(4):
            if (path[i][j] != path[i+1][j] and flipFlag != 1):
                flipFlag = 1
                currCost += (4 - j)
                builder += "|"
            builder += path[i][j]

        if path[i][0] != "4":
            heuristic = "4"
        elif path[i][1] != "3":
            heuristic = "3"
        elif path[i][2] != "2":
            heuristic = "2"
        elif path[i][3] != "1":
            heuristic = "1"
        else:
            heuristic = "0"
    
        builder += (" g=" + str(cost) + ", " + "h=" + heuristic)
        cost += currCost
        output.append(builder)
    
    # Goal State (final append)
    builder = "Final State: "
    for i in range(4):
        builder += path[n-1][i]
    builder += (" g=" + str(cost) + ", " + "h=" + str(0))
    output.append(builder)  
    return output

# Returns heuristic of a passed in state
def getFutureHeuristic(data):
    if data[0] != "4":
        return "4"
    if data[1] != "3":
        return "3"
    if data[2] != "2":
        return "2"
    if data[3] != "1":
        return "1"
    return "0"

## Search Algorithms
# Recursive DFS, the recursion is a little messy but I believe the algorithm works
def depthFirstSearch(pancakeStack, visited = None, path = None):
    # Init Variables, visited is a list of visited nodes. Path is current solution path.
    if visited == None:
        visited = []
    if path == None:
        path = []

    # If the goal has been found keep returning the path (exit recursion)
    if pancakeStack.goalFlag == 1:
        return path
    else:
        # Append Current Node To Visited and Current Path
        visited.append(pancakeStack.queue)
        path.append(pancakeStack.queue)

        # Check if current node is goal state
        if pancakeStack.goalTest() == True:
            pancakeStack.goalFlag = 1
            return path

        # Generate Fringe
        fringe = pancakeStack.generateChildrenStates()
        fringe.sort(reverse = True) # Sort fringe max -> min , this will ensure the largest child breaks the tie

        # Recursive DFS on leftmost non-visted child, prefering the largest child (to break tie)
        for i in range(3):
            if (fringe[i] not in visited):    
                #print(pancakeStack.printFlip(i, pancakeStack.getCost(i), pancakeStack.getHeuristic(i)))
                pancakeStack.queue = fringe[i]
                depthFirstSearch(pancakeStack, visited, path)
        
        # If all children have been visited, go up a level.
        if pancakeStack.goalFlag != 1:
            path.pop()
            pancakeStack.queue = path[-1]
            depthFirstSearch(pancakeStack, visited, path)
        # Exit Route For Recursion
        elif pancakeStack.goalFlag == 1:
            return path
    return

# Non recursive UCS
def uniformCostSearch(pancakeStack):
    # Init Variables
    path = []
    fringe = []
    cost = 0

    # Init fringe with start state as a multidimensional array with path and cost respectively
    fringe.append([[pancakeStack.queue], cost])

    # While the goal state has not been reached
    while pancakeStack.goalFlag != 1:
        # For every potential path on the fringe
        for i in range(len(fringe)):

            # Find the last visited node of said path
            pancakeStack.queue = fringe[i][0][-1]

            # Check if current state is goal state, if it is update path to current route
            if (pancakeStack.goalTest() == True):
                if i != 0: break # break if not the cheapest route 
                # Update path to current (cheapest) route
                path = fringe[i][0]
                pancakeStack.goalFlag = 1
                break

            # Generate the potential children of that state
            childrenStates = pancakeStack.generateChildrenStates()

            # Add children and their costs as a new pathway on the fringe
            for j in range(3):
                # Create a copy of current path and cost as new entry on the fringe
                fringe.append(copy.deepcopy([fringe[i][0], fringe[i][1]]))
                
                # Update newly created copy with child state
                fringe[-1][0].append(childrenStates[j])
                fringe[-1][1] += pancakeStack.getCost(childrenStates[j])
        
            # Delete current expanded state from fringe (only maintain currently expanding routes)
            fringe.pop(i)

        # Sort fringe by lowest cost, breaking any ties by ensuring the largest end node is first
        # After sorting the lowest costing choice will be index 0.
        fringe.sort(key = lambda x: x[0][-1], reverse = True)
        fringe.sort(key = lambda x: x[1])
    return path

# Non Recursive Greedy Search
def greedySearch(pancakeStack):
    # Init Variables
    path = []
    fringe = []
    heuristic = pancakeStack.getHeuristic()

    # Init fringe with start state as a multidimensional array with path and cost respectively
    fringe.append([[pancakeStack.queue], heuristic])

    # While the goal state has not been reached
    while pancakeStack.goalFlag != 1:
        # For every potential path on the fringe
        for i in range(len(fringe)):

            # Find the last visited node of said path
            pancakeStack.queue = fringe[i][0][-1]

            # Check if current state is goal state, if it is update path to current route
            if pancakeStack.goalTest() == True:
                if i != 0: break # break if not the cheapest route 
                # Update path to current (cheapest) route
                path = fringe[i][0]
                pancakeStack.goalFlag = 1
                break

            # Generate the potential children of that state
            childrenStates = pancakeStack.generateChildrenStates()

            # Add children and their heuristic values as a new pathway on the fringe
            for j in range(3):
                # Create a copy of current path and cost as new entry on the fringe
                fringe.append(copy.deepcopy([fringe[i][0], fringe[i][1]]))
                
                # Update newly created copy with child state
                fringe[-1][0].append(childrenStates[j])
                fringe[-1][1] = getFutureHeuristic((childrenStates[j]))
        
            # Delete current expanded state from fringe (only maintain currently expanding routes)
            fringe.pop(i)

        # Sort fringe by lowest heuristic, breaking any ties by ensuring the largest end node is first
        # After sorting the lowest heuristic choice will be index 0.
        fringe.sort(key = lambda x: x[0][-1], reverse = True)
        fringe.sort(key = lambda x: x[1])
    return path

# Non recursive A* Search
def aStarSearch(pancakeStack):
    # Init Variables
    path = []
    fringe = []
    cost = 0
    heuristic = pancakeStack.getHeuristic()

    # Init fringe with start state as a multidimensional array with path, cost, and heuristic respectively
    fringe.append([[pancakeStack.queue], cost, heuristic])
    
    # While the goal state has not been reached
    while pancakeStack.goalFlag != 1:
        # For every potential path on the fringe
        for i in range(len(fringe)):

            # Find the last visited state of said path
            pancakeStack.queue = fringe[i][0][-1]

            # Check if current state is goal state, if it is update path to current route
            if pancakeStack.goalTest() == True:
                if i != 0: break # break if not the cheapest route 
                # Update path to current (cheapest) route
                path = fringe[i][0]
                pancakeStack.goalFlag = 1
                break

            # Generate the potential children of that state
            childrenStates = pancakeStack.generateChildrenStates()

            # Add children and their costs as a new pathway on the fringe
            for j in range(3):
                # Create a copy of current path and cost as new entry on the fringe
                fringe.append(copy.deepcopy([fringe[i][0], fringe[i][1], fringe[i][2]]))
                
                # Update newly created copy with child state
                fringe[-1][0].append(childrenStates[j])
                fringe[-1][1] += pancakeStack.getCost(childrenStates[j])
                fringe[-1][2] = getFutureHeuristic(childrenStates[j])
        
            # Delete current expanded state from fringe (only maintain currently expanding routes)
            fringe.pop(i)

        # Sort fringe by lowest total cost + heuristic, breaking any ties by ensuring the largest end node is first
        # After sorting the lowest costing choice will be index 0
        fringe.sort(key = lambda x: x[0][-1], reverse = True)
        fringe.sort(key = lambda x: x[1] + int(x[2])) # Total cost + Heuristic
    return path

## Main Function
if __name__ == '__main__':

    # Initialize Variables + Objects
    userIn = ''

    # Start the program
    print('Welcome to Pancake Sort! Please follow the prompts below. To quit enter q at any point.')
    while(userIn != "q" and userIn !="Q"):
        pancakeStack = PancakeQueue()

        print("Available Algorithms: \n")
        print("\t d - DFS \n")
        print("\t u - UCS \n")
        print("\t g - Greedy \n")
        print("\t a - A* \n")

        userIn = input("Please enter the order of pancakes (1-4) followed by the desirede algorithm code e.g. 1234a: ")
        
        # Take care of most input errors / ensure format is ####X
        rex = re.compile("^[1-4]{4}[a,d,g,u]{1}$")

        while not rex.match(userIn):
            if userIn == "q" or userIn == "Q":
                exit()
            else:
                print("Incorrect input format, please try again...")
                userIn = input("Please enter the order of pancakes (1-4) followed by the desired algorithm code e.g. 1234a: ")

        if (userIn != "q" and userIn !="Q"):
            # Build priority queue based on pancake ordering.
            pancakeStack.push(userIn[0]) 
            pancakeStack.push(userIn[1]) 
            pancakeStack.push(userIn[2]) 
            pancakeStack.push(userIn[3])
            print("Starting Stack: ", end = "")
            print(pancakeStack)

            # Choose correct algorithm function based on user input.
            algorithm = userIn[4]
            if algorithm == "d":
                print("Depth First Search Solution: ")
                path = printPath(depthFirstSearch(pancakeStack)) # DFS
            if algorithm == "u":
                print("Uniform Cost Search Solution: ") 
                path = printPath(uniformCostSearch(pancakeStack)) # UCS
            if algorithm == "g":
                print("Greedy Search Solution: ") 
                path = printPath(greedySearch(pancakeStack)) # Greedy
            if algorithm == "a": 
                print("A* Search Solution: ") 
                path = printPath(aStarSearch(pancakeStack)) # A*

            # Print Algorithm Output To Console
            for i in range(len(path)):
                print(path[i])

            print() # Newline
            userIn = input("Continue? Press The Enter Key...")
            if (userIn == 'q' or userIn =='Q'):
                break

    # Empty Queue + Exit
    while not pancakeStack.isEmpty(): pancakeStack.delete()
    exit()
