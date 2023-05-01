#import packages
import mesa
import mesa_geo as mg
import geopandas as gpd
from shapely.geometry import Point
import random
random.seed(3)
# from landlab import RasterModelGrid
# from landlab.components import TidalFlowCalculator


#import agents
from agents import *
from space import *
    
#set up class for model
class OysterModel(mesa.Model):
    
    """A model class for oysters"""

    #path to reef file and unique reef ID
    reefs_data = "data/oyster_reef_buf.gpkg"
    unique_id = "OBJECTID"

    #define init parameters
    def __init__(self):
        #self.num_oysters = N #number of oysters (int)
        # self.harvest_rate = harvest_rate #proportion of oysters to take (between 0 and 1)
        # self.num_safe_reefs = num_safe_reefs #how many reefs are sanctuary reefs
        self.space = SeaBed(crs = "epsg:3857")
        self.schedule = mesa.time.RandomActivation(self)
        self.step_count = 1
        self.current_id = 0
        self.ind_per_super_a = (2142.45 * 9) #num oysters per cell area times nine for moore neighborhood

        #add crs for space
        self.space.set_elevation_layer(crs = "epsg:3857")

        # #init RasterModelGrid object for landlab
        # self.rmg = RasterModelGrid((self.space.raster_layer.height, 
        #                             self.space.raster_layer.width),
        #                            1.157226984026, 
        #                            (-9051628.873678505, 3492744.042225802))
        # self.rmg.add_field("topographic__elevation", #add elevation data
        #                    self.space.raster_layer.get_raster("elevation"))
        
        # #init empty field for roughness values
        # self.rough = self.rmg.add_empty("node", 'mannings_n')

        # #store roughness vals
        # self.sand_roughness = 0.02
        # self.oyster_roughness = 0.035  

        # #store tidal period for depth
        # self.tidal_period = 43482.58

        reef_data = gpd.read_file("data/oyster_reef_buf.gpkg")
        
        #create reef agents
        ac = mg.AgentCreator(
            Reef, 
            model = self,
            agent_kwargs = {
                "poly" : reef_data
                }
            )
        self.reef_agents = ac.from_file(
            self.reefs_data, 
            unique_id = self.unique_id,
            set_attributes = True
            )
        
        #add reef agents to space
        self.space.add_agents(self.reef_agents)

        #add shells to each reef, proportional to reef size
        for agent in self.reef_agents:
            for i in range(round((agent.SHAPE_Area * 2785)/self.ind_per_super_a)):
                #create agent
                this_shell = Shell(
                    unique_id = "shell_" + str(self.next_id()),
                    model = self,
                    geometry = self.point_in_reef(agent),
                    crs =  self.space.crs,
                    shell_length = random.randint(1,300)
                )
                #add oyster agents to raster, agent layer, and scheduler
                self.space.add_oyster(this_shell)
                self.space.add_agents(this_shell)
                self.schedule.add(this_shell)

        #add oysters to each reef, proportional to reef size
        for agent in self.reef_agents:
            for i in range(round((agent.SHAPE_Area * 1620)/self.ind_per_super_a)):
                 #create agent
                this_oyster = Oyster(
                    unique_id = "oyster_" + str(self.next_id()),
                    model = self,
                    geometry = self.point_in_reef(agent),
                    crs =  self.space.crs,
                    birth_reef = agent,
                    home_reef = agent,
                    age = random.randint(1, 3649)
                )
                #add oyster agents to raster, agent layer, and scheduler
                self.space.add_oyster(this_oyster)
                self.space.add_agents(this_oyster)
                self.schedule.add(this_oyster)

        #add reef agents to schedule after oysters
        for agent in self.reef_agents:
            self.schedule.add(agent)

        #init data collector
        self.running = True
        
        #tell data collector what to collect
        self.datacollector = mesa.DataCollector(
            agent_reporters = {"type" : "type",
                                #oyster metrics
                                "age": lambda a: a.age if a.type == "Oyster" else None,
                                "energy": lambda a: a.energy if a.type == "Oyster" else None,
                                "daily_energy": lambda a: a.daily_energy if a.type == "Oyster" else None,
                                "fertility": lambda a: a.fertility if a.type == "Oyster" else None,
                                "shell_length_mm": lambda a: a.shell_length_mm if a.type == "Oyster" else None,
                                "dry_biomass": lambda a: a.dry_biomass if a.type == "Oyster" else None,
                                "wet_biomass": lambda a: a.wet_biomass if a.type == "Oyster" else None,
                                "mortality_prob": lambda a: a.mortality_prob if a.type == "Oyster" else None,
                                "elevation": lambda a: a.elevation if a.type == "Oyster" else None,
                                "pct_time_underwater": lambda a: a.pct_time_underwater if a.type == "Oyster" else None,
                                "total_shell_weight": lambda a: a.total_shell_weight if a.type == "Reef" else None,
                                #reef metrics
                                "oyster_count": lambda a: a.oyster_count if a.type == "Reef" else None,
                                "total_mm_growth": lambda a: a.total_mm_growth if a.type == "Reef" else None
                                },
            #get oyster lifespan                    
            tables = {"Lifespan": [lambda a: a.unique_id if a.type == "Oyster" else None, 
            lambda a: a.age if a.type == "Oyster" else None]}
            )
    
    #create while loop to return point in reef
    def point_in_reef (self, random_reef):
        minx, miny, maxx, maxy = random_reef.geometry.bounds
        pnt = Point(0,0)
        while not random_reef.geometry.contains(pnt):
            pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        return pnt
    
    #function to convert shell length to shell weight
    def length_to_weight (self, shell_length_mm):
        dry_biomass = 9.6318 * (10**-6) * (shell_length_mm**2.743)
        wet_biomass =  (dry_biomass * 5.6667) + dry_biomass 
        shell_weight = wet_biomass * 3.4
        return shell_weight
   
    #define step
    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
        self.step_count += 1
        self.datacollector.collect(self)
        # #add oysters to rmg
        # self.rmg.add_field("num_oysters",
        #                    self.space.raster_layer.get_raster("num_oysters_in_cell"),
        #                    clobber = True)
        # #store roughness vals in attribute of rastermodel grid
        # self.rough[self.rmg.at_node["num_oysters"] == 0] = self.sand_roughness
        # self.rough[self.rmg.at_node["num_oysters"] > 0] = self.oyster_roughness
        # #map roughness to link
        # r_link = self.rmg.map_mean_of_link_nodes_to_link("mannings_n")
        # #init tidal flow calculator
        # tfc = TidalFlowCalculator(self.rmg, 
        #                           tidal_range = 1.289919, 
        #                           tidal_period = self.tidal_period, 
        #                           roughness = r_link)
        # #run the tidal flow calc
        # tfc.run_one_step()
        # #get innudiation rate
        # rate = tfc.calc_tidal_inundation_rate()
        self.space._recreate_rtree()  # Recalculate spatial tree, because agents are moving??
        
        #stop step after 5 yr
        if self.step_count == (365 * 5) + 1:
            self.running = False

    #define run model function
    def run_model(self, steps):
         for i in range(steps):
            self.step()

       

