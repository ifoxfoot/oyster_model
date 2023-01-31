#import mesa package
import mesa
import mesa_geo as mg

#import model and agent
from model import *
from agents import *

#set up visualization
def agent_portrayal(agent):
    portrayal = dict()
    if isinstance(agent, Oyster):
        if agent.energy > 1.5:
            portrayal["color"] = "red"
        else:
            portrayal["color"] = "grey"
    else: portrayal["color"] = "Green"
    return portrayal

map_element = mg.visualization.MapModule(agent_portrayal)

#server code
server = mesa.visualization.ModularServer(
    OysterModel, [map_element], "Oyster Model", {"N": 100, "harvest_rate": 20}
)

#code to launch
server.port = 8521  # The default
server.launch()