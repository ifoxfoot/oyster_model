#this script contains the code to produce mesa agents
#there are three types of agents: shells, oysters, and reefs
#agents are creating using mesa-geo's geo agent class
#agent classes have two main components. 
#A component that sets initial values and a component that defines what they do at each time step
#in this model a time step is one day

#import packages
import mesa_geo as mg
import random
import rasterio as rio
from rasterio.features import rasterize
import pandas as pd
import numpy as np
import geopandas as gpd

#import functions that determine oyster energy, growth, fertility and mortality
#these functions are all sored in the "functions" folder
from functions.energy_fun import *
from functions.shell_length_fun import *
from functions.fertility_fun import *
from functions.mortality_fun import *

#import model. The model is a type of class from mesa
from model import *

#set up class for shells
class Shell(mg.GeoAgent):

    """Shell Agent Class"""

    #function to initialize attributes
    def __init__(self, unique_id, model, geometry, crs, shell_length, age = 1):
        super().__init__(unique_id, model, geometry, crs)
        #set general attributes
        self.type = "Shell"
        self.shell_length = shell_length
        self.og_shell_length = shell_length  #stores the starting shell length
        self.shell_weight = self.model.length_to_weight(self.shell_length)
        self.age = age

        #geometry #IRIS LOOK INTO WHY THIS IS MIRRORED OVER X AND Y
        row, col = rio.transform.rowcol(
            self.model.space.raster_layer.transform, 
            self.geometry.x, self.geometry.y)
        self.x = col
        self.y = row - self.model.space.raster_layer.height - 1 

    #This function defines what the shell does at every time step   (1 day)  
    def step(self):
        
        #increment age up
        self.age += 1
        
        #shell degrades reducing shell length and weight
        self.shell_length = (-0.08219178*self.age) + self.og_shell_length
        self.shell_weight = self.model.length_to_weight(self.shell_length)

        #if shell is less than one mm remove from model
        if self.shell_length < 1:
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.space.remove_oyster(self)
    

#set up class for oyster agent
class Oyster(mg.GeoAgent):
    
    """Oyster Agent Class"""
   
    #function to define initial attribute values
    def __init__(self, unique_id, model, geometry, crs, birth_reef, home_reef, age = 0):
         super().__init__(unique_id, model, geometry, crs)
         self.type = "Oyster"

         #position
         self.geometry = geometry
         row, col = rio.transform.rowcol(
            self.model.space.raster_layer.transform, 
            self.geometry.x, self.geometry.y)
         self.x = col
         self.y = row - self.model.space.raster_layer.height - 1
         
         #innundiation time
         self.elevation = self.model.space.raster_layer.cells[self.x][-self.y].elevation
         self.pct_time_underwater = max(min(-0.496*self.elevation + 0.499, 1), 0)

         #demographics
         self.age = age
         self.birth_reef = birth_reef
         self.home_reef = home_reef
         self.energy = random.randint(1,10) #start with random energy level between 1 and 10
         self.shell_length_mm = 0.08219178 * self.age #found using line between (0,0) and (3650-max age, 300-max size)
         self.dry_biomass = 9.6318 * (10**-6) * (self.shell_length_mm**2.743)
         self.wet_biomass =  (self.dry_biomass * 5.6667) + self.dry_biomass
         self.shell_weight = self.model.length_to_weight(self.shell_length_mm)
         self.fertility = None
         self.reproduced = False
         self.mortality_prob = None
         self.daily_energy = None
         self.mort_cause = "alive"
         self.model.counts["alive"] += 1 #count all alive oysters when they are initialized 

         #init energy list
         self.energy_list = []

         #establish reproductive days (two periods in summer)
         self.reproductive_days = list(range(203, 210)) + list(range(212, 215))

    #define what happens at each step (1 day)   
    def step(self):

        #set status to alive
        self.status = "alive"

        # #innundiation time
        # self.elevation = self.model.space.raster_layer.cells[self.x][-self.y].elevation
        # self.pct_time_underwater = max(min(-0.496*self.elevation + 0.499, 1), 0)
        
        #add 1 day to age
        self.age += 1

        #calculate energy gain
        self.daily_energy = energy_gain(
                self.age, 
                self.home_reef.do,
                self.home_reef.tss, 
                self.home_reef.tss_list, 
                self.home_reef.tds, 
                self.home_reef.tds_list, 
                self.home_reef.temp, 
                self.home_reef.temp_list
            )
        self.energy += (self.daily_energy * self.pct_time_underwater) #energy gain weighted by time underwater
        self.energy_list.append(self.daily_energy * self.pct_time_underwater)

        #energy loss
        self.energy -= (1.2 * self.pct_time_underwater) #I wonder if this makes sense to have a constant value that doesn't vary with temperature, respiration goes down when its cold

        #calculate growth metrics
        self.shell_length_mm += shell_length_gain(self.shell_length_mm, self.energy)
        self.dry_biomass = 9.6318 * (10**-6) * (self.shell_length_mm**2.743)
        self.wet_biomass =  (self.dry_biomass * 5.6667) + self.dry_biomass 
        self.shell_weight = self.model.length_to_weight(self.shell_length_mm)

        #calculate death probability
        self.mortality_prob = mort_prob(
            self.age, 
            self.home_reef.tds, 
            self.home_reef.tds_list, 
            self.home_reef.tss, 
            self.home_reef.tss_list, 
            self.home_reef.temp, 
            self.home_reef.temp_list, 
            self.home_reef.do, 
            self.home_reef.do_list
            )
        
        #if conditions met, kill off
        if ((self.energy < 0) or 
            (self.age > 3650) or 
            (random.random() < (self.mortality_prob * self.pct_time_underwater)) or 
            ((self.model.step_count >= 8) and all(v == 0 for v in self.energy_list[-8:])) or
            self.pct_time_underwater <= 0.20 #made up this num
            ):
                #record the cause of mortality
                if self.energy < 0:
                    self.mort_cause = "no_energy"
                elif self.age > 3650:
                    self.mort_cause = "old_age"
                elif ((self.model.step_count >= 8) and all(v == 0 for v in self.energy_list[-8:])):
                    self.mort_cause = "no_energy_eight_days"
                elif self.pct_time_underwater <= 0.20:
                    self.mort_cause = "out_of_water"
                else: 
                    self.mort_cause = "mortality"

                #add dead oyster to dead oyster count
                self.model.counts[self.mort_cause] += 1

                #remove agent from model and scheduler 
                self.model.space.remove_agent(self)
                self.model.schedule.remove(self)

                #convert dead oysters to shells
                new_shell = Shell(
                    unique_id = "shell_" + str(self.unique_id),
                    model = self.model,
                    geometry = self.geometry, 
                    crs = self.model.space.crs,
                    shell_length = self.shell_length_mm
                    )

                #add shell agents to grid and scheduler
                self.model.space.add_agents(new_shell)
                self.model.schedule.add(new_shell)
        
        #if oyster didn't die, count it as alive
        else: self.model.counts["alive"] += 1
            
        # #harvest on day 298 if home reef is not sancuary, according to harves rate
        # if (self.status == "alive") & (self.model.step_count%298 == 0) & (self.home_reef.sanctuary_status == False) & (random.random() < self.model.harvest_rate):
        #     self.status = "harvested"
        #     self.model.space.remove_agent(self)
        #     self.model.schedule.remove(self)
        
        #reproduction
        if ((self.status == "alive") and
            (self.reproduced == False) and
            any(self.model.step_count%i == 0 for i in self.reproductive_days)):

            #calculate number of babies oyster would have (surviving spat that settle in model area)
            self.fertility = n_babies(
                self.age, 
                self.home_reef.do, 
                self.home_reef.tss, 
                self.home_reef.tds, 
                self.home_reef.temp)
            
            #set reproduced to T for rest of spawning period. Oysters can only reproduce once per each spawning period
            if self.fertility > 0:
                self.reproduced = True

            #create new oysters
            for i in range(self.fertility):
                area_list = [a.SHAPE_Area for a in self.model.reef_agents]
                choice = random.choices(self.model.reef_agents, weights = area_list)
                #get random reef for new oyster to settle on
                random_reef = choice[0]
                
                #create oyster
                baby_oyster = Oyster(
                    unique_id = "oyster_" + str(self.model.next_id()),
                    model = self.model,
                    geometry = self.model.point_in_reef(random_reef), 
                    crs = self.model.space.crs,
                    birth_reef = self.home_reef,
                    home_reef = random_reef,
                    age = 0
                )
            
                #add oyster agents to raster, agent layer, and scheduler
                self.model.space.add_oyster(baby_oyster)
                self.model.space.add_agents(baby_oyster)
                self.model.schedule.add(baby_oyster)

        #reset reproduction val for next spawning period
        if self.model.step_count%211 == 0:
            self.reproduced = False

        #reset reproduction val for next spawning period
        if self.model.step_count%216 == 0:
            self.reproduced = False


#set up class for ReefAgent
class Reef(mg.GeoAgent):

    """Reef Agent"""

    def __init__(
        self, unique_id, model, geometry, crs, poly
        # sanctuary_status
    ):
        super().__init__(unique_id, model, geometry, crs)
        self.type = "Reef"
        # self.sanctuary_status = sanctuary_status #this code is optional if sancuary reefs are being considered
        
        #read in water quality data
        self.data = pd.read_csv("data/wq_perams_late.csv")

        self.poly = poly
        self.shape = poly.loc[poly['OBJECTID'] == self.unique_id]

        #create lists for multi-step effects
        self.tss_list = []
        self.temp_list = []
        self.tds_list = []
        self.do_list = []
        #init env values
        self.do = self.data.loc[1, 'mean_do']
        self.tss = self.data.loc[1, 'pred_tss'] 
        self.temp = self.data.loc[1, 'mean_temp']
        self.tds = self.data.loc[1, 'mean_sal']
        #init growth stuff
        self.shell_weight_gain = None
        self.total_mm_growth = 0

    def step(self):
        #get oyster count for each reef
        self.oyster_count = len(list(a for a in self.model.space.get_intersecting_agents(self) 
                                     if isinstance(a, Oyster)))
        #get oyster count for each reef
        self.shell_count = len(list(a for a in self.model.space.get_intersecting_agents(self) 
                                     if isinstance(a, Shell)))
        #get shell to oyster ratio for each reef
        self.shell_to_oyster = self.shell_count/(self.oyster_count + 0.1) #add 0.1 to prevent dividing by 0
        #get total wieght of oyster shells
        self.total_shell_weight = self.model.space.get_intersecting_agents(self)
        #get new environmental variables by reading next row down
        self.do = self.data.loc[self.model.step_count + 1, 'mean_do']
        self.tss = self.data.loc[self.model.step_count + 1, 'pred_tss'] 
        self.temp = self.data.loc[self.model.step_count + 1, 'mean_temp']
        self.tds = self.data.loc[self.model.step_count + 1, 'mean_sal']
        #store variables in list
        self.tss_list.append(self.tss)
        self.temp_list.append(self.temp)
        self.tds_list.append(self.tds)
        self.do_list.append(self.do)
        #limit list length so we don't have to store lots of data per agent
        self.tss_list = self.tss_list[-14:]
        self.temp_list = self.temp_list[-7:]
        self.tds_list = self.tds_list[-7:]
        self.do_list = self.do_list[-7:]

        #get first day shell weight so we know how much reef is adding
        if self.model.step_count == 1:
            init_shell_weight = [a.shell_weight for a in self.model.space.get_intersecting_agents(self) 
                                       if isinstance(a, (Oyster, Shell))]
            self.initial_shell_weight = sum(init_shell_weight)

        #natural recruitment
        if (self.model.step_count > 0) and (self.model.step_count%211 == 0 or
                                            self.model.step_count%216 == 0 ):
           
           #if oyster density is low, replenish with recruits
            if ((self.SHAPE_Area * 1620)/self.model.ind_per_super_a) > self.oyster_count:
                for i in range(round(((self.SHAPE_Area * 1620)/self.model.ind_per_super_a) - self.oyster_count)):
                    #create oyster
                    baby_oyster = Oyster(
                        unique_id = "oyster_" + str(self.model.next_id()),
                        model = self.model,
                        geometry = self.model.point_in_reef(self), 
                        crs = self.model.space.crs,
                        birth_reef = "out_of_bounds",
                        home_reef = self,
                        age = 0
                    )
            
                    #add oyster agents to raster, agent layer, and scheduler
                    self.model.space.add_oyster(baby_oyster)
                    self.model.space.add_agents(baby_oyster)
                    self.model.schedule.add(baby_oyster)

        #once a month get total shell weight
        if self.model.step_count%30 == 0:
            #get shell weight 
            shell_weights = [a.shell_weight for a in self.model.space.get_intersecting_agents(self) 
                                       if isinstance(a, (Oyster, Shell))]
            self.shell_weight_gain = sum(shell_weights) - self.initial_shell_weight 
            #amount to raise reef by (convert g to kg)
            self.mm_of_growth = ((((self.shell_weight_gain * self.model.ind_per_super_a)/1000)/self.SHAPE_Area)/0.731) - self.total_mm_growth #total_mm_growth starts at 0
            self.total_mm_growth += self.mm_of_growth #then growth is added
            #assign reef growth value to polygon (convert mm to m)
            vals = ((geom, (self.mm_of_growth/1000)) for geom in self.shape.geometry)
            #define transform
            transform = rio.transform.from_bounds(*self.model.space.raster_layer.total_bounds, 
                                                  width=self.model.space.raster_layer.width, 
                                                  height=self.model.space.raster_layer.height)
            # create an empty raster to store the output
            image = np.zeros((self.model.space.raster_layer.height, self.model.space.raster_layer.width), dtype=np.float32) 
            #rasterize polygon
            ras = rasterize(shapes=vals, out=image, transform=transform)
            #add growth vals to elevation layer
            elev = self.model.space.raster_layer.get_raster("elevation")
            new_elev = ras + elev
            self.model.space.raster_layer.apply_raster(new_elev, 
                                                       attr_name = "elevation")

    #get reef identity
    def __repr__(self):
        return "Reef " + str(self.unique_id)

