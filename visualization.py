#import the model and mesa package
from model import *
import mesa

#set up visualization
def agent_portrayal(agent):
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

#init grid
grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)  


#server code
server = mesa.visualization.ModularServer(
    OysterModel, [grid], "Oyster Model", {"N": 100, "width": 10, "height": 10}
)

#code to launch
server.port = 8521  # The default
server.launch()