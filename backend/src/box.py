from mesa import Agent

class Box(Agent):
    
    UNORDERED = 0
    PROCCESSING = 1
    STACKED = 2
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.state = Box.UNORDERED
        self.robot = None
        self.height = 1
    def step(self):
        pass