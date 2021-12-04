from mesa import Agent, Model
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid as PathGrid
from src.box import Box

class Robot(Agent):
    SEARCHING = 0
    CARRYING_A_BOX = 1
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.state = Robot.SEARCHING
        self.lastPosBox = (0, 0)
        self.path = [1]
        self.isPathCompleted = True

    def step(self):

        next_moves = self.model.grid.get_neighborhood(self.pos, moore=False)
        next_move = self.random.choice(next_moves)

        # random movements to search a box
        if not self.state == Robot.CARRYING_A_BOX:

            if not next_move in self.model.positions_used:
                self.model.grid.move_agent(self, next_move)
            elif not next_move in self.model.stackedBoxes:
                self.state = Robot.CARRYING_A_BOX
                self.model.positions_used.remove(next_move)
                self.model.grid.get_cell_list_contents([next_move])[0].state = Box.PROCCESSING
                self.model.grid.get_cell_list_contents([next_move])[0].robot = self
                self.lastPosBox = next_move
        else:
            # pathfinding movements
            if self.isPathCompleted:
                self.generate_path()
                # print(self.model.stackedBoxes)
                # print(self.path)
                if len(self.path) > 0:
                    self.model.grid.move_agent(self, self.path[0])
                    self.isPathCompleted = False
            else:
                if len(self.path) <= 2:
                    # path isPathCompleted
                    self.isPathCompleted = True
                    self.put_box()

                    # statistics
                    self.model.stackedBoxesN += 1
                    if self.model.stackedBoxesN + 6 == self.model.numberOfBoxes:
                        print("Tiempo necesario: ", self.model.steps)
                        print("Número de movimientos: ", self.model.steps * 5)
                else:
                    # print("caminando")
                    self.path.pop(0)
                    self.model.grid.move_agent(self, self.path[0])

    def put_box(self):
        # box state updated
        box = self.model.grid.get_cell_list_contents([self.lastPosBox])[0]
        lastBox = self.model.grid.get_cell_list_contents([self.path[-1]])[0]
        box.state = Box.STACKED
        box.robot = None 
        box.pos = self.path[-1] 
        lastBox.height += 1 
        box.height = lastBox.height
        # robot state updated
        self.state = Robot.SEARCHING

    def generate_path(self):

        self.matrix = []

        for i in range(10):
            a = []
            for j in range(10):
                if (i, j) in self.model.positions_used:
                    a += [0]
                else:
                    a += [1]
            self.matrix.append(a)

        self.maze = PathGrid(matrix=self.matrix)

        stack = self.model.random.choice(self.model.stackedBoxes)
        stackedBox = self.model.grid.get_cell_list_contents([stack])[0]
        # print(self.model.stackedBoxes)
        while stackedBox.height >= 4:
            stack = self.model.random.choice(self.model.stackedBoxes)
            stackedBox = self.model.grid.get_cell_list_contents([stack])[0]

        # define end and start

        start = self.maze.node(self.pos[0], self.pos[1])
        # print(start)
        end = self.maze.node(stack[0], stack[1])
        # print(self.matrix)
        
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, self.maze)

        # print(path)
        self.path = path.copy()
        # print(self.model.positions_used)