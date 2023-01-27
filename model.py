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
    def __init__(self, N):
        self.num_oysters = N
        self.space = mg.GeoSpace(warn_crs_conversion=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.step_count = 0
        self.current_id = 0

        #create reef agents
        ac = mg.AgentCreator(Reef, model=self)
        reef_agents = ac.from_file(
            self.reefs, unique_id = self.unique_id
            )
        self.space.add_agents(reef_agents)

        #create oyster agents
        ac_population = mg.AgentCreator(
            Oyster,
            model = self,
            crs = self.space.crs,
            age = random.randint(1, 3649)
        )

        #generate location, add oysters to location
        for i in range(self.num_oysters):
            #get random reef
            random_reef =  self.random.randint(
                0, len(reef_agents) - 1
            )
            #generate point where agent is located within random reef
            center_x, center_y = reef_agents[
                random_reef
            ].geometry.centroid.coords.xy
            this_bounds = reef_agents[random_reef].geometry.bounds
            spread_x = int(
                this_bounds[2] - this_bounds[0]
            ) 
            spread_y = int(this_bounds[3] - this_bounds[1])
            this_x = center_x[0] + self.random.randint(0, spread_x) - spread_x / 2
            this_y = center_y[0] + self.random.randint(0, spread_y) - spread_y / 2
            this_oyster = ac_population.create_agent(
                Point(this_x, this_y), i,
            )
            #add oyster agents to grid and scheduler
            self.space.add_agents(this_oyster)
            self.schedule.add(this_oyster)

        #add reef agents after oysters created
        for agent in reef_agents:
            self.schedule.add(agent)

        #init data collector
        self.running = True
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
