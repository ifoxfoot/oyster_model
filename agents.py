#import packages
import mesa_geo as mg
import random
import rasterio as rio
from rasterio.features import rasterize
import pandas as pd

#import funs
from functions.energy_fun import *
from functions.shell_length_fun import *
from functions.fertility_fun import *
from functions.mortality_fun import *

#import model
from model import *


#set up class for shells
class Shell(mg.GeoAgent):

    """Shell Agent"""

    def __init__(self, unique_id, model, geometry, crs, shell_length):
        super().__init__(unique_id, model, geometry, crs)
        self.type = "Shell"
        self.shell_length = shell_length
        self.shell_weight = self.model.length_to_weight(self.shell_length)

        #geometry 
        row, col = rio.transform.rowcol(
            self.model.space.raster_layer.transform, 
            self.geometry.x, self.geometry.y)
        self.x = col
        self.y = row - self.model.space.raster_layer.height - 1
        
    def step(self):
        #shell degredation
        self.shell_length -= (self.shell_length * .001)
        self.shell_weight = self.model.length_to_weight(self.shell_length)

        #if less than one mm remove from model
        if self.shell_length < 1:
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.space.remove_oyster(self)
    

#set up class for oyster agent
class Oyster(mg.GeoAgent):
    
    """An oyster with assigned age, energy, and size."""
   
    #define init values
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
         self.energy = random.randint(0,10)
         self.shell_length_mm = 0.08219178 * self.age #found using line between (0,0) and (3650-max age, 300-max size)
         self.dry_biomass = 9.6318 * (10**-6) * (self.shell_length_mm**2.743)
         self.wet_biomass =  (self.dry_biomass * 5.6667) + self.dry_biomass
         self.shell_weight = self.model.length_to_weight(self.shell_length_mm)
         self.fertility = 0
         self.mortality_prob = 0
         self.daily_energy = 0

         #init energy list
         self.energy_list = []

    #define what happens at each step      
    def step(self):

        #set status to alive
        self.status = "alive"
        
        #age
        self.age += 1

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
        self.energy += (self.daily_energy * self.pct_time_underwater)
        self.energy_list.append(self.daily_energy)
       
        # #energy gain if under water
        # if self.model.space.raster_layer.cells[self.x][-self.y].water_level > 0:
        #     daily_energy = energy_gain(
        #         self.age, 
        #         self.home_reef.do,
        #         self.home_reef.tss, 
        #         self.home_reef.tss_list, 
        #         self.home_reef.tds, 
        #         self.home_reef.tds_list, 
        #         self.home_reef.temp, 
        #         self.home_reef.temp_list
        #     )
        #     self.energy += daily_energy
        #     self.energy_list.append(daily_energy)
        #     self.enery_gained = 1
        # else:
        #     self.energy_gained = 0

        #energy loss
        self.energy -= 1.2

        #growth
        self.shell_length_mm += shell_length_gain(self.shell_length_mm, self.energy)
        self.dry_biomass = 9.6318 * (10**-6) * (self.shell_length_mm**2.743)
        self.wet_biomass =  (self.dry_biomass * 5.6667) + self.dry_biomass 
        self.shell_weight = self.model.length_to_weight(self.shell_length_mm)

        #death probabiliyt NOT ADDED INTO DEATH IF STATEMENT YET
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
            (random.random() < self.mortality_prob * self.pct_time_underwater) or 
            ((self.model.step_count >= 8) and all(v == 0 for v in self.energy_list[-8:]))
            ):
            self.status = "dead"
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
            
        # #harvest on day 298 if home reef is not sancuary, according to harves rate
        # if (self.status == "alive") & (self.model.step_count%298 == 0) & (self.home_reef.sanctuary_status == False) & (random.random() < self.model.harvest_rate):
        #     self.status = "harvested"
        #     self.model.space.remove_agent(self)
        #     self.model.schedule.remove(self)

        #establish reproductive days
        reproductive_days = list(range(203, 210)) + list(range(212, 215))
        
        #reproduction
        if (self.status == "alive") and any(self.model.step_count%i == 0 for i in reproductive_days):

            #get fertility
            self.fertility = n_babies(
                self.age, 
                self.home_reef.do, 
                self.home_reef.tss, 
                self.home_reef.tds, 
                self.home_reef.temp)

            #create new oysters
            for i in range(self.fertility):
                #get random reef
                random_reef = random.choice(self.model.reef_agents)
                
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


#set up class for ReefAgent
class Reef(mg.GeoAgent):

    """Reef Agent"""

    def __init__(
        self, unique_id, model, geometry, crs, 
        # sanctuary_status
    ):
        super().__init__(unique_id, model, geometry, crs)
        self.type = "Reef"
        # self.sanctuary_status = sanctuary_status
        self.data = pd.read_csv("data/wq_perams_10apr23.csv")

        #create lists for multi-step effects
        self.tss_list = []
        self.temp_list = []
        self.tds_list = []
        self.do_list = []
        #init env values
        self.do = self.data.loc[1, 'mean_do']
        self.tss = self.data.loc[1, 'pred_tss'] #needs to be converted to tss still
        self.temp = self.data.loc[1, 'mean_temp']
        self.tds = self.data.loc[1, 'mean_sal']
        #init shell weight
        self.total_shell_weight = None

    def step(self):
        #get oyster count
        self.oyster_count = len(list(self.model.space.get_intersecting_agents(self)))
        #get total wieght of oyster shells
        self.total_shell_weight = self.model.space.get_intersecting_agents(self)
        #get new environmental variables
        self.do = self.data.loc[self.model.step_count + 1, 'mean_do']
        self.tss = self.data.loc[self.model.step_count + 1, 'mean_turb'] #needs to be converted to tss still
        self.temp = self.data.loc[self.model.step_count + 1, 'mean_temp']
        self.tds = self.data.loc[self.model.step_count + 1, 'mean_sal']
        #store variables in list
        self.tss_list.append(self.tss)
        self.temp_list.append(self.temp)
        self.tds_list.append(self.tds)
        self.do_list.append(self.do)
        #limit list length
        self.tss_list = self.tss_list[-14:]
        self.temp_list = self.temp_list[-7:]
        self.tds_list = self.tds_list[-7:]
        self.do_list = self.do_list[-7:]
        #once a year get total shell weight
        if self.model.step_count%4 == 0:
            #get shell weight 
            shell_weights = [a.shell_weight for a in self.model.space.get_intersecting_agents(self) 
                                       if isinstance(a, (Oyster, Shell))]
            self.total_shell_weight = sum(shell_weights)
            #amount to raise reef by
            self.mm_of_growth = (((self.total_shell_weight * 100000)/1000)/self.SHAPE_Area)/0.731
            #assign reef growth value to polygon
            vals = ((geom, self.mm_of_growth) for geom in self.geometry)
            #define transform
            transform = rio.transform.from_bounds(*self.total_bounds, 
                                                  width=self.model.space.raster_layer.width, 
                                                  height=self.model.space.raster_layer.width)
            #rasterize polygon
            ras = rasterize(shapes=vals, out=self.model.space.raster_layer, transform=transform)
            #add growth vals to elevation layer
            self.model.space.raster_layer.new_elevation += ras

    #get reef identity
    def __repr__(self):
        return "Reef " + str(self.unique_id)

