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
        self.current_id = N

        #create reef agents
        ac = mg.AgentCreator(Reef, model = self)
        self.reef_agents = ac.from_file(
            self.reefs, unique_id = self.unique_id
            )
        self.space.add_agents(self.reef_agents)

        #generate location, add oysters to location
        for i in range(self.num_oysters):
            #get random reef
            random_reef =  self.random.randint(
                0, len(self.reef_agents) - 1
            )
            #create while loop to return point in reef
            def point_in_reef (random_reef):
                    minx, miny, maxx, maxy = self.reef_agents[random_reef].geometry.bounds
                    pnt = Point(0,0)
                    while not self.reef_agents[random_reef].geometry.contains(pnt):
                        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
                    return pnt
        
            #create agent
            this_oyster = Oyster(
                unique_id = "oyster_" + str(i),
                model = self,
                geometry = point_in_reef(random_reef),
                crs =  self.space.crs,
                home_reef = random_reef,
                age = random.randint(1, 3649)
            )
            #add oyster agents to grid and scheduler
            self.space.add_agents(this_oyster)
            self.schedule.add(this_oyster)

        #add reef agents after oysters created
        for agent in self.reef_agents:
            self.schedule.add(agent)

        #init data collector
        self.running = True
        
        self.datacollector = mesa.DataCollector(
            # agent_reporters = {"Oyster": energy(Oyster),
                                # "energy": "energy",
                                # "fertility": "fertility",
                                # "shell_length_mm": "shell_length_mm",
                                # "dry_biomass": "dry_biomass",
                                # "wet_biomass": "wet_biomass",
                                # "mortality_prob": "mortality_prob"
                                # }
            # tables = {"Lifespan": ["unique_id", "age"]}
            )

    #definte step
    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()
        self.step_count += 1
