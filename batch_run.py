
#import library 
import pandas as pd

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

# First, we filter the results
one_episode_energy = results_df[(results_df.N == 500) & (results_df.iteration == 2)]
# Then, print the columns of interest of the filtered data frame
print(
    one_episode_energy.to_string(
        index=False, columns=["Step", "AgentID", "Energy"], max_rows=25
    )
)