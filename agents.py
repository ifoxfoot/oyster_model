#import packages
import mesa_geo as mg
import random
from shapely.geometry import Point

#import funs
from functions.energy_fun import *
from functions.shell_length_fun import *
from functions.fertility_fun import *
from functions.mortality_fun import *

#set up class for oyster agent
class Oyster(mg.GeoAgent):
    
    """An oyster with assigned age, energy, and size."""
   
    #define init values
    def __init__(self, unique_id, home_reef, model, geometry, crs, age = 0):
         super().__init__(unique_id, model, geometry, crs)
         self.home_reef = home_reef
         self.age = age
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

        #set living to true
        living = True
        
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

        #death
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
        
        if (self.energy < 0) or (self.age > 3650) or ((self.model.step_count >= 8) and all(v == 0 for v in self.energy_list[-8:])):
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            living = False

        #establish reproductive days
        reproductive_days = list(range(203, 210)) + list(range(212, 215))
        
        #reproduction
        if living and any(self.model.step_count%i == 0 for i in reproductive_days):

            #get fertility
            self.fertility = n_babies(
                self.age, 
                self.home_reef.do, 
                self.home_reef.tss, 
                self.home_reef.tds, 
                self.home_reef.temp)

            #create new oysters
            for i in range(self.fertility):
                babyOyster = Oyster(self.model.next_id(), self.model)
                #get random reef
                random_reef =  self.random.randint(
                0, len(self.model.reef_agents) - 1
                )
                #generate point where agent is located within random reef
                center_x, center_y = self.model.reef_agents[random_reef].geometry.centroid.coords.xy
                this_bounds = self.model.reef_agents[random_reef].geometry.bounds
                spread_x = int(this_bounds[2] - this_bounds[0]) 
                spread_y = int(this_bounds[3] - this_bounds[1])
                this_x = center_x[0] + self.random.randint(0, spread_x) - spread_x / 2
                this_y = center_y[0] + self.random.randint(0, spread_y) - spread_y / 2
                this_oyster = babyOyster.create_agent(
                    Point(this_x, this_y), 
                    unique_id = i, 
                    home_reef = random_reef
                )
            
                #add oyster agents to grid and scheduler
                self.space.add_agents(this_oyster)
                self.schedule.add(this_oyster)

#set up class for ReefAgent
class Reef(mg.GeoAgent):

    """Reef Agent"""

    def __init__(
        self, unique_id, model, geometry, crs
    ):
        super().__init__(unique_id, model, geometry, crs)
        #create lists for multi-step effects
        self.tss_list = []
        self.temp_list = []
        self.tds_list = []
        self.do_list = []

    def step(self):
        #get environmental variables
        do = random.randint(150, 340)*0.01
        tss = random.randint(0, 300)
        temp = random.randint(4, 33)
        tds = random.randrange(10,27)
        #store variables in list
        self.tss_list.append(tss)
        self.temp_list.append(temp)
        self.tds_list.append(tds)
        self.do_list.append(do)
        #limit list length
        self.tss_list = self.tss_list[-14:]
        self.temp_list = self.temp_list[-7:]
        self.tds_list = self.tds_list[-7:]
        self.do_list = self.do_list[-7:]

    #get reef identity
    def __repr__(self):
        return "Reef " + str(self.unique_id)

