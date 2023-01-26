#import packages
import mesa
import mesa_geo as mg
from shapely.geometry import Point
import random

#import agents
from agents import *
    
#set up class for model
class OysterModel(mesa.Model):
    
    """A model class for oysters in the Chesapeake Bay"""

    reefs = "data/Schulte_reefs.shp"
    unique_id = "Id"

    #define init parameters
    def __init__(self, N, width, height):
        self.num_agents = N
        self.space = mg.GeoSpace(warn_crs_conversion=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.step_count = 0
        self.current_id = 0
        
        # Create agents
        for i in range(self.num_agents):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            age = random.randint(1, 3649)
            oyster = Oyster(self.next_id(), self, age)
            self.grid.place_agent(oyster, (x, y))
            self.schedule.add(oyster)

        #init data collector
        self.datacollector = mesa.DataCollector(
            agent_reporters = {"energy": "energy",
                              "fertility": "fertility",
                              "shell_length_mm": "shell_length_mm",
                              "dry_biomass": "dry_biomass",
                              "wet_biomass": "wet_biomass",
                              "mortality_prob": "mortality_prob"
                              },
            tables = {"Lifespan": ["unique_id", "age"]}
            )

    #definte step
    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()
        self.step_count += 1
