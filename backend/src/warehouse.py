from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder
from src.box import Box
from src.robot import Robot

class Warehouse(Model):
    def __init__(self):
        super().__init__()


        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(10, 10, torus=False)
        self.steps = 0


        self.place_boxes()
        self.place_agents()
        # self.generate_matrix()
        # print(self.matrix)

    def step(self):
        self.schedule.step()
        self.steps += 1
        # stop simulation
        if self.steps == 500:
            self.running = False

    def get_random_position(self, agent):
        random_position = (self.random.randrange(0, 9), self.random.randrange(0, 9))

        while random_position in self.positions_used:
            random_position = (self.random.randrange(0, 9), self.random.randrange(0, 9))

        if agent == 1:
            self.positions_used.append(random_position)
        else:
            self.agents_positions.append(random_position)
        # self.matrix[random_position[0]][random_position[1]] = 1

        return random_position 


    def place_agents(self):

        self.agents_positions = []

        # init agents
        sam = Robot(self, self.get_random_position(0))
        wall_e = Robot(self, self.get_random_position(0))
        r2i2 = Robot(self, self.get_random_position(0))
        redbot = Robot(self, self.get_random_position(0))
        wi_fido = Robot(self, self.get_random_position(0))

        # place agents
        self.grid.place_agent(sam, sam.pos)
        self.grid.place_agent(wall_e, wall_e.pos)
        self.grid.place_agent(r2i2, r2i2.pos)
        self.grid.place_agent(redbot, redbot.pos)
        self.grid.place_agent(wi_fido, wi_fido.pos)

        # add agents
        self.schedule.add(sam)
        self.schedule.add(wall_e)
        self.schedule.add(r2i2)
        self.schedule.add(redbot)
        self.schedule.add(wi_fido)

    def place_boxes(self):
        
        self.positions_used = []
        self.stackedBoxesN = 0

        # get random number of boxes

        self.numberOfBoxes = self.random.randrange(20, 30)
        
        # place all boxes
        for x in range(self.numberOfBoxes):
            box = Box(self, self.get_random_position(1))
            self.grid.place_agent(box, box.pos)
            self.schedule.add(box)
        
        # choose random stacks
        self.stackedBoxes = self.random.choices(self.positions_used, k=6)
        # for x in self.stackedBoxes:
        #     self.grid.get_cell_list_contents([x])[0].state = Box.STACKED

