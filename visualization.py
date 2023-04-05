#import mesa package
import mesa
import mesa_geo as mg

#import model and agent
from model import *
from agents import *

#set up sliders for model parames
model_params = {
    "N": mesa.visualization.Slider("Number of Oysters", 
                                   value = 5000, min_value = 1000, max_value = 20000, step =100),
    "harvest_rate": mesa.visualization.Slider(
        "Harvest Rate",  value = .5, min_value = 0, max_value = 1, step = 0.1
    ),
    "num_safe_reefs": mesa.visualization.Slider(
        "Number of Sanctuary Reefs", value = 5, min_value = 0, max_value = 10, step = 1
    ),
}

#define how agents will be shown
def agent_portrayal(agent):
    if isinstance(agent, mg.GeoAgent):
        if isinstance(agent, Reef):
            return {
                "Color": "Blue",
                "Layer": 0
            }
        elif isinstance(agent, Shell):
            return {
                "color": "Gray",
                "radius": 0.001,
                "Layer": 1
            }
        elif isinstance(agent, Oyster):
            return {
                "color": "Green",
                "radius": 0.001,
                "Layer": 1
            }
            # if agent.energy_gained == 1:
            #     return {
            #         "color": "Green",
            #         "radius": .01,
            #         "Layer": 2
            #     }
            # else:
            #     return {
            #         "color": "Red",
            #         "radius": 0.01,
            #         "Layer": 2
            #     }
    elif isinstance(agent, SeaBedCell):
        return (agent.water_level, agent.water_level, agent.water_level, 1)


#create map element
map_element = mg.visualization.MapModule(agent_portrayal)


#server
server = mesa.visualization.ModularServer(
    OysterModel, [map_element], "Oyster Model", model_params = model_params
)

#launch server to port
server.launch()