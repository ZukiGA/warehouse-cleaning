import flask
from flask.json import jsonify
import uuid
import os
from src.warehouse import Warehouse
from src.box import Box

simulations = {}

app = flask.Flask(__name__)

@app.route("/simulation", methods=["POST"])
def create():
    global simulations
    id = str(uuid.uuid4())
    simulations[id] = Warehouse()
    # print(simulations[id].schedule.agents)
    return "ok", 201, {'Location': f"/simulation/{id}", "Items": len(simulations[id].schedule.agents) - 5}

@app.route("/simulation/<id>", methods=["GET"])
def queryState(id):
    global model
    model = simulations[id]
    model.step()
    agents = []
    for agent in model.schedule.agents:
        if isinstance(agent, Box) and agent.robot:
            position = agent.robot.pos 
            agents.append({"type": type(agent).__name__, "state": agent.state, "x": position[0], "y": position[1], "z": 1})
        elif isinstance(agent, Box) and agent.state == 2:
            agents.append({"type": type(agent).__name__, "state": agent.state, "x": agent.pos[0], "y": agent.pos[1], "z": agent.height})
        else:
            agents.append({"type": type(agent).__name__, "state": agent.state, "x": agent.pos[0], "y": agent.pos[1], "z": 1})
    return jsonify({"Items": agents})

app.run()