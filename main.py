from copy import deepcopy
import csv
import heapq
from queue import Queue

class Node:
    def __init__(self, rushHourPuzzle, parent=None, action="", c=1, h=1):
        self.state = rushHourPuzzle
        self.parent = parent
        self.action = action
        self.g = 0 if not self.parent else self.parent.g + c
        self.setF(heuristic)
#returns the path of states from the current node to the root node
    def getPath(self):
        states = []
        node = self
        while node != None:
            states.append(node.state)
            node = node.parent
        return states[::-1]
 #gets (return) the sequence of actions from the current node to the root node
    def getSolution(self):
        actions = []
        node = self
        while node != None:
            actions.append(node.action)
            node = node.parent
        return actions[::-1]
    
    def setF(self, heuristic):
        heuristics = {1:self.h1(), 2:self.h2()}
        self.f



class RushHourPuzzle:
    def __init__(self, puzzle_file):
        # Initialize the Rush Hour puzzle Board
        self.setVehicles(puzzle_file)
        self.setBoard()

    def setVehicles(self, puzzle_file):
        with open(puzzle_file) as file:
            csvreader = csv.reader(file)
            w, h = next(csvreader)
            self.board_width, self.board_height = int(w), int(h)
            self.vehicles = []
            self.walls = []
            for line in csvreader:
                if line[0] == "#":
                    self.walls.append((int(line[1]), int(line[2])))
                else:
                    id, x, y, orientation, length = line
                    vehicle = {
                        "id": id,
                        "x": int(x),
                        "y": int(y),
                        "orientation": orientation,
                        "length": int(length),
                    }
                    self.vehicles.append(vehicle)

    def setBoard(self):
        self.board = [
            [" " for _ in range(self.board_width)] for _ in range(self.board_height)
        ]
        for x, y in self.walls:
            self.board[y][x] = "#"
        for vehicle in self.vehicles:
            x, y = vehicle["x"], vehicle["y"]
            if vehicle["orientation"] == "H":
                for i in range(vehicle["length"]):
                    self.board[y][x + i] = vehicle["id"]
            else:
                for i in range(vehicle["length"]):
                    self.board[y + i][x] = vehicle["id"]

    # check if the red car is at the goal position
    def isGoal(self):
        for vehicle in self.vehicles:
            if vehicle["id"] == "X" and vehicle["x"] == self.board_width - 2:
                return True
        return False

    # Generate the successors
    def successorFunction(self):
        succs = list()
        for index, vehicle in enumerate(self.vehicles):
            x_position = vehicle["x"]
            y_position = vehicle["y"]

            # check if the vehicle is oriented horizontal
            if vehicle["orientation"] == "H":
                # move left if it's not on the edge of the board and it's not blocked by another vehicle
                if x_position > 0 and self.board[y_position][x_position - 1] == " ":
                    successor = deepcopy(self)
                    successor.vehicles = deepcopy(self.vehicles)
                    # update the vehicle's position
                    successor.vehicles[index]["x"] = x_position - 1
                    # update the board
                    successor.setBoard()
                    succs.append(("{}:L".format(vehicle["id"]), successor))

                # move right if it's not on the edge of the board and it's not blocked by another vehicle
                if (
                    x_position + vehicle["length"] < self.board_width
                    and self.board[y_position][x_position + vehicle["length"]] == " "
                ):
                    successor = deepcopy(self)
                    successor.vehicles = deepcopy(self.vehicles)
                    # update the vehicle's position
                    successor.vehicles[index]["x"] = x_position + 1
                    # update the board
                    successor.setBoard()
                    succs.append(("{}:R".format(vehicle["id"]), successor))

            # check if the vehicle is oriented vertical
            else:
                # move up if it's not on the edge of the board and it's not blocked by another vehicle
                if y_position > 0 and self.board[y_position - 1][x_position] == " ":
                    successor = deepcopy(self)
                    successor.vehicles = deepcopy(self.vehicles)
                    # update the vehicle's position
                    successor.vehicles[index]["y"] = y_position - 1
                    # update the board
                    successor.setBoard()
                    succs.append(("{}:U".format(vehicle["id"]), successor))

                # move down if it's not on the edge of the board and it's not blocked by another vehicle
                if (
                    y_position + vehicle["length"] < self.board_height
                    and self.board[y_position + vehicle["length"]][x_position] == " "
                ):
                    successor = deepcopy(self)
                    successor.vehicles = deepcopy(self.vehicles)
                    # update the vehicle's position
                    successor.vehicles[index]["y"] = y_position + 1
                    # update the board
                    successor.setBoard()
                    succs.append(("{}:D".format(vehicle["id"]), successor))
        return succs

#################################################################################################################################""
def a_star(puzzle):
    # Initialize the open and closed lists
    open = []
    closed = set()

    # Add the start node
    start = Node(puzzle)
    heapq.heappush(open, (start.g + puzzle.heuristic(), start))

    # Loop until there are no more nodes to expand
    while open:
        # Get the next node
        node = heapq.heappop(open)[1]

        # Check if the node is the goal
        if node.isGoal():
            return node.getSolution()

        # Add the node to the closed list
        closed.add(node.state)

        # Expand the node
        for action, successor in node.state.successorFunction():
            # Check if the successor is already in the closed list
            if successor in closed:
                continue

            # Check if the successor is already in the open list
            if successor in [n[1].state for n in open]:
                continue

            # Add the successor to the open list
            heapq.heappush(open, (successor.g, successor))

    # No solution found
    
    return None


def main():
    puzzle = RushHourPuzzle("C:/Users/dell/Desktop\MIV-Algerie/S1/RP/TP/1.csv")
    solution = a_star(puzzle)
    if solution:
        print("Solution found with {} moves:".format(len(solution)))
        for action in solution:
            print("  {}".format(action))
    else:
        print("No solution found")


if __name__ == "__main__":
    main()