#import packages
import mesa_geo as mg
import random
from shapely.geometry import Point

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
        self.shell_length = shell_length
        self.type = "Shell"
        
    def step(self):
        self.shell_length =- self.shell_length * .001

#set up class for oyster agent
class Oyster(mg.GeoAgent):
    
    """An oyster with assigned age, energy, and size."""
   
    #define init values
    def __init__(self, unique_id, model, geometry, crs, birth_reef, home_reef, age = 0):
         super().__init__(unique_id, model, geometry, crs)
         self.type = "Oyster"
         self.age = age
         self.birth_reef = birth_reef
         self.home_reef = self.model.space.agents[home_reef]
         self.energy = random.randint(0,10)
         self.shell_length_mm = random.randint(1, 300)
         self.dry_biomass = 9.6318 * (10**-6) * (self.shell_length_mm**2.743)
         self.wet_biomass =  (self.dry_biomass * 5.6667) + self.dry_biomass
         self.fertility = 0
         self.mortality_prob = 0

         #init energy list
         self.energy_list = []

    #define what happens at each step      
    def step(self):

        #set status to alive
        self.status = "alive"
        
        #age
        self.age += 1
       
        #energy gain
        daily_energy = energy_gain(
            self.age, 
            self.home_reef.do,
            self.home_reef.tss, 
            self.home_reef.tss_list, 
            self.home_reef.tds, 
            self.home_reef.tds_list, 
            self.home_reef.temp, 
            self.home_reef.temp_list
        )
        self.energy += daily_energy
        self.energy_list.append(daily_energy)

        #energy loss
        self.energy -= 1.2

        #growth
        self.shell_length_mm += shell_length_gain(self.shell_length_mm, self.energy)
        self.dry_biomass = 9.6318 * (10**-6) * (self.shell_length_mm**2.743)
        self.wet_biomass =  (self.dry_biomass * 5.6667) + self.dry_biomass 

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
        if (self.energy < 0) or (self.age > 3650) or ((self.model.step_count >= 8) and all(v == 0 for v in self.energy_list[-8:])):
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
            
        #harvest on day 298 if home reef is not sancuary, according to harves rate
        if (self.status == "alive") & (self.model.step_count%298 == 0) & (self.home_reef.sanctuary_status == False) & (random.random() < self.model.harvest_rate):
            self.status = "harvested"
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)

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
                random_reef =  self.random.randint(
                0, len(self.model.reef_agents) - 1
                )
                #create while loop to return point in reef
                def point_in_reef (random_reef):
                        minx, miny, maxx, maxy = self.model.reef_agents[random_reef].geometry.bounds
                        pnt = Point(0,0)
                        while not self.model.reef_agents[random_reef].geometry.contains(pnt):
                            pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
                        return Point(self.model.space.raster_layer.transform * (pnt.x, pnt.y))
                
                #create oyster
                baby_oyster = Oyster(
                    unique_id = "oyster_" + str(self.model.next_id()),
                    model = self.model,
                    geometry = point_in_reef(random_reef), 
                    crs = self.model.space.crs,
                    birth_reef = self.home_reef,
                    home_reef = random_reef,
                    age = 0
                )
            
                #add oyster agents to grid and scheduler
                self.model.space.add_agents(baby_oyster)
                self.model.schedule.add(baby_oyster)


#set up class for ReefAgent
class Reef(mg.GeoAgent):

    """Reef Agent"""

    def __init__(
        self, unique_id, model, geometry, crs, sanctuary_status
    ):
        super().__init__(unique_id, model, geometry, crs)
        self.type = "Reef"
        self.sanctuary_status = sanctuary_status

        #create lists for multi-step effects
        self.tss_list = []
        self.temp_list = []
        self.tds_list = []
        self.do_list = []
        #init env values
        self.do = random.randint(150, 340)*0.01
        self.tss = random.randint(0, 300)
        self.temp = random.randint(4, 33)
        self.tds = random.randrange(10,27)

    def step(self):
        #get step count
        self.oyster_count = len(list(self.model.space.get_intersecting_agents(self)))
        #get new environmental variables
        self.do = random.randint(150, 340)*0.01
        self.tss = random.randint(0, 300)
        self.temp = random.randint(4, 33)
        self.tds = random.randrange(10,27)
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

    #get reef identity
    def __repr__(self):
        return "Reef " + str(self.unique_id)

