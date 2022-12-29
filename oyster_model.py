#this tutorial uses the mesa package
import mesa
import random


#set up class for agent
class Oyster(mesa.Agent):
    
    """An agent with randomly assigned initial energy & age."""
   
    #define init values
    def __init__(self, unique_id, model):
         super().__init__(unique_id, model)
         self.age = random.randint(0, 3649)
         self.energy = random.randint(1,10)

    #define what happens at each step      
    def step(self):
        living = True
        self.age += 1
        self.energy += random.randint(-5, 5)
       
        # Death
        if self.energy < 0 or self.age > 3650:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            living = False

        if living & self.energy >= 1.5 and self.age > 365:
            for i in random.randint(1,6):
                babyOyster = Oyster(
                    self.model.next_id(), self.model, self.energy, self.age
                )
                self.model.grid.place_agent(babyOyster, self.pos)
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
        
        # Create agents
        for i in range(self.num_agents):
            a = Oyster(i, self)
            self.schedule.add(a)
            
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    #definte step
    def step(self):
        """Advance the model by one step."""
        self.schedule.step()

