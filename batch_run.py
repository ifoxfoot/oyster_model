
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
    max_steps=365 * 4,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

#convert results to df
results_df = pd.DataFrame(results)
print(results_df.keys())

# #get reef agents
# iteration_one = results_df[results_df.type == "Reef"]

# #plot
# sns.lineplot(data=iteration_one, x='Step', y='oyster_count', hue='AgentID')
# plt.xlabel('step')
# plt.ylabel('Total mm Growth')
# plt.title("Modeled Change In Reef Elevation After 5 Years")
# plt.show()

#plot
# sns.lineplot(data=iteration_one, x='Step', y='total_mm_growth', hue='AgentID')
# plt.xlabel('step')
# plt.ylabel('Total mm Growth')
# plt.title("Modeled Change In Reef Elevation After 5 Years")
# plt.show()

# sns.lineplot(data=iteration_one, x='Step', y='oyster_count', hue='AgentID')
# plt.xlabel('step')
# plt.ylabel('Number of Oysters and Shells')
# plt.title("Oyster and Shell Population over 5 Years")
# plt.show()

#get oyster agents
# iteration_one = results_df[results_df.type == "Oyster"]

pops = results_df.groupby(['Step', 'type']).size().reset_index(name='counts')
sns.lineplot(data=pops, x='Step', y='counts', hue='type')
plt.xlabel('step')
plt.legend()
plt.show()

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


