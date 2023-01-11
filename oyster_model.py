#import packages
import mesa
import random

#import funs
from energy_funs import *

#establish reproductive days
reproductive_days = list(range(203, 210)) + list(range(212, 215))

#set up class for agent
class Oyster(mesa.Agent):
    
    """An agent with assigned age."""
   
    #define init values
    def __init__(self, unique_id, model, age = 0):
         super().__init__(unique_id, model)
         self.energy = random.randint(0,10)
         self.age = age
         self.living = True

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
        do = random.randint(25, 250)*0.01
        tss = random.randint(0, 5000)
        temp = random.randint(0, 40)
        tds = random.randrange(5,37)

        #store variables in list
        self.tss_list.append(tss)
        self.temp_list.append(temp)
        self.tds_list.append(tds)

        #age
        self.age += 1
       
        #energy gain
        if self.age < 365:
            energy_gain = (2.8 * do_juvi(do) * tds_juvi(tds, self.tds_list) * tss_juvi(tss, self.tss_list) * temp_juvi(temp, self.temp_list))
        else:
            energy_gain = (2.8 * do_adult(do) * tds_adult(tds, self.tds_list) * tss_adult(tss, self.tss_list) * temp_adult(temp, self.temp_list))

        #store energy gain
        self.energy += energy_gain
        self.energy_list.append(energy_gain)

        #energy loss
        self.energy -= 1.2

        # Death
        if (self.energy < 0) or (self.age > 3650) or ((self.model.step_count >= 8) and all(v == 0 for v in self.energy_list[-8:])):
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            living = False

        #reproductive potential depending on age
        if self.age < 1095 and random.random() < 0.03:
            female = True
        elif self.age >= 1095 and random.random() < 0.75:
            female = True
        else:
            female = False

        #establish reproductive days
        reproductive_days = list(range(203, 210)) + list(range(212, 215))
        
        #reproduction
        if living & female & (self.age > 365) and any(self.model.step_count%i == 0 for i in reproductive_days):
            
            for i in range(3):
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

    #definte step
    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
        self.step_count += 1
