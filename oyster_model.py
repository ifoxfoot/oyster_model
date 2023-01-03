#this tutorial uses the mesa package
import mesa
import random


#set up class for agent
class Oyster(mesa.Agent):
    
    """An agent with randomly assigned initial energy & age."""
   
    #define init values
    def __init__(self, unique_id, model, age = 0):
         super().__init__(unique_id, model)
         self.energy = random.randint(1,10)
         self.age = age

    #define what happens at each step      
    def step(self):
        living = True
        self.age += 1
        self.energy += random.randint(-5, 5)
       
        # Death
        if (self.energy < 0) or (self.age > 3650):
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            living = False

        #reproduction
        if living & (self.age > 365) and (self.energy > 2) and self.model.step_count%50 == 0 : 
            for i in range(3):
                babyOyster = Oyster(
                    self.model.next_id(), self.model
                )
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
