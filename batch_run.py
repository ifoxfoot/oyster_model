
#import library 
import mesa
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#import model
from model import *

#set params
params = {}

#batch run
results = mesa.batch_run(
    OysterModel,
    parameters=params,
    iterations=1,
    max_steps=1825,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

#convert results to df
results_df = pd.DataFrame(results)
print(results_df.keys())

#get reef agents
iteration_one = results_df[results_df.type == "Reef"]

#plot
sns.plot(iteration_one.total_mm_growth, color = ,label = "mm of growth")
plt.xlabel('step')
plt.legend()
plt.show()

#get oyster agents
# iteration_one = results_df[results_df.type == "Oyster"]

# means = iteration_one.groupby('Step').mean("energy")
# plt.plot((means.energy), label = "mean energy")
# plt.xlabel('step')
# plt.legend()
# plt.show()

# means = iteration_one.groupby('Step').mean("age")
# plt.plot((means.age), label = "mean age")
# plt.xlabel('step')
# plt.legend()
# plt.show()

# means = iteration_one.groupby('Step').mean("shell_length_mm")
# plt.plot((means.shell_length_mm), label = "mean shell length")
# plt.xlabel('step')
# plt.legend()
# plt.show()

#first filter the results for one iteration one agent to look at oyster metrics
#iteration_one = results_df[(results_df.AgentID == "oyster_1094")]

#plot things (Oyster)
# plt.plot(iteration_one.Step, iteration_one.shell_length_mm, label = "shell_length_mmt")
# plt.show()
#plt.plot(iteration_one.Step, iteration_one.dry_biomass, label = "dry_biomass")
#plt.plot(iteration_one.Step, iteration_one.wet_biomass, label = "wet_biomass")
#plt.plot(iteration_one.Step, iteration_one.shell_length_mm, label = "shell length (mm)")
#plt.plot(iteration_one.Step, iteration_one.energy, label = "energy")
#plt.plot(iteration_one.Step, iteration_one.fertility, label = "fertility")
#plt.plot(iteration_one.Step, iteration_one.mortality_prob, label = "mortality prob")


