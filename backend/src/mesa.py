# from mesa.visualization.modules import CanvasGrid
# from mesa.visualization.ModularVisualization import ModularServer
# from warehouse import Warehouse
# from robot import Robot


# def agent_portrayal(agent):
#     if isinstance(agent, Robot):
#         if agent.state == 1:
#             return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Red", "Layer": 0}        
#         else: 
#             return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Blue", "Layer": 0}
#     elif agent.state == 0:
#         return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Gray", "Layer": 0}
#     elif agent.state == 2:
#         return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Green", "Layer": 0}
#     else:
#         return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "White", "Layer": 0}


# grid = CanvasGrid(agent_portrayal, 10, 10, 450, 450)

# server = ModularServer(Warehouse, [grid], "Robots", {})
# server.port = 8521
# server.launch()