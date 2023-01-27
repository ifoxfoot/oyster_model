#import mesa package
import mesa
import mesa_geo as mg

#import model and agent
from model import *
from agents import *

#set up visualization
def agent_portrayal(agent):
    if isinstance(agent, Oyster):
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                     "r": 0.5}

    if agent.energy > 1.5:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal

map_element = mg.visualization.MapModule(agent_portrayal)

#server code
server = mesa.visualization.ModularServer(
    OysterModel, [map_element], "Oyster Model", {"N": 100}
)

#code to launch
server.port = 8521  # The default
server.launch()