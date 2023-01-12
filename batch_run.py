
#import library 
import mesa
import random
import pandas as pd
import matplotlib.pyplot as plt

#import model
from oyster_model import *

#set params
params = {"width": 10, "height": 10, "N": 500}

#batch run
results = mesa.batch_run(
    OysterModel,
    parameters=params,
    iterations=5,
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

#convert results to df
results_df = pd.DataFrame(results)
print(results_df.keys())

#first filter the results for one iteration one agent
iteration_one = results_df[(results_df.iteration == 1) & (results_df.AgentID == random.randint(1,500))]

#plot energy and shell
plt.plot(iteration_one.Step, iteration_one.Energy, label = "energy")
plt.plot(iteration_one.Step, iteration_one.shell_length_mm, label = "shell length (mm)")
plt.xlabel('step')
plt.legend()
plt.show()
