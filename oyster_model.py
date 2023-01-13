#import packages
import mesa
import random

#import funs
from energy_fun import *
from shell_length_fun import *
from fertility_fun import *

#establish reproductive days
reproductive_days = list(range(203, 210)) + list(range(212, 215))

#set up class for agent
class Oyster(mesa.Agent):
    
    """An agent with assigned age, energy, and size."""
   
    #define init values
    def __init__(self, unique_id, model, age = 0):
         super().__init__(unique_id, model)
         self.age = age
         self.energy = random.randint(0,10)
         self.shell_length_mm = random.randint(1, 300)
         self.dry_biomass = 9.6318 * (10**-6) * (self.shell_length_mm**2.743)
         self.wet_biomass =  (self.dry_biomass * 5.6667) + self.dry_biomass
         self.fertility = 0
         
         #create lists for multi-step effects
         self.energy_list = []
         self.tss_list = []
         self.temp_list = []
         self.tds_list = []

    #define what happens at each step      
    def step(self):

        #set living to true
        living = True
        
        #get environmental variables
        do = random.randint(150, 340)*0.01
        tss = random.randint(0, 300)
        temp = random.randint(4, 33)
        tds = random.randrange(10,27)

        #store variables in list
        self.tss_list.append(tss)
        self.temp_list.append(temp)
        self.tds_list.append(tds)

        #age
        self.age += 1
       
        #energy gain
        daily_energy = energy_gain(
            self.age, do, tss, self.tss_list, tds, self.tds_list, temp, self.temp_list
        )
        self.energy += daily_energy
        self.energy_list.append(daily_energy)

        #energy loss
        self.energy -= 1.2

        #growth
        self.shell_length_mm += shell_length_gain(self.shell_length_mm, self.energy)
        self.dry_biomass = 9.6318 * (10**-6) * (self.shell_length_mm**2.743)
        self.wet_biomass =  (self.dry_biomass * 5.6667) + self.dry_biomass 

        # Death
        if (self.energy < 0) or (self.age > 3650) or ((self.model.step_count >= 8) and all(v == 0 for v in self.energy_list[-8:])):
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            living = False

        #establish reproductive days
        reproductive_days = list(range(203, 210)) + list(range(212, 215))
        
        #reproduction
        if living and any(self.model.step_count%i == 0 for i in reproductive_days):

            #get fertility
            self.fertility = n_babies(self.age, do, tss, tds, temp)

            #create new oysters
            for i in range(self.fertility):
                babyOyster = Oyster(self.model.next_id(), self.model)
                x = self.random.randrange(self.model.grid.width)
                y = self.random.randrange(self.model.grid.height)
                self.model.grid.place_agent(babyOyster, (x, y))
                self.model.schedule.add(babyOyster)

    
#set up class for model
class OysterModel(mesa.Model):
    
    """A model with some number of agents."""

    #define init parameters
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
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
                              "wet_biomass": "wet_biomass"
                              },
            tables = {"Lifespan": ["unique_id", "age"]}
            )

    #definte step
    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()
        self.step_count += 1
