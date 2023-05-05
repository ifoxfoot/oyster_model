
#import library 
import mesa
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#set figure size to auto adjust
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


#import model
from model import *

#set params
params = {}

#batch run
results = mesa.batch_run(
    OysterModel,
    parameters=params,
    iterations=1,
    max_steps=365*5,
    number_processes=1,
    data_collection_period=1, 
    display_progress=True,
)

#convert results to df
results_df = pd.DataFrame(results)
print(results_df.keys())

#get reef agents
reefs = results_df[results_df.type == "Reef"]


#change in elevation
#filter by step/30
thirty_steps = reefs[reefs['Step'] % 30 == 0]
ax = sns.lineplot(data=thirty_steps, x='Step', y='mm_growth', hue='AgentID', palette="Set1")
plt.xlabel('Model Step (1 Day)')
plt.ylabel('Elevation\nChange (mm)', rotation = 0)
ax.yaxis.set_label_coords(-0.2, 0.5)
plt.legend(title="Reef ID")
plt.title("Modeled Change In Reef Elevation Over 5 Years")
plt.savefig('outputs/reef_elevation.png', dpi = 600)
plt.show()

#
ax = sns.lineplot(data=reefs, x='Step', y='total_mm_growth', hue='AgentID', palette="Set1")
plt.xlabel('Model Step (1 Day)')
plt.ylabel('Elevation\nChange (mm)', rotation = 0)
ax.yaxis.set_label_coords(-0.2, 0.5)
plt.legend(title="Reef ID")
plt.title("Modeled Change In Reef Elevation Over 5 Years")
plt.savefig('outputs/reef_elevation_cummulative.png', dpi = 600)
plt.show()

# #counts of oysters and shells
pops = results_df.groupby(['Step', 'type']).size().reset_index(name='counts')
ax = sns.lineplot(data=pops, x='Step', y='counts', hue='type')
plt.xlabel('Model Step (1 Day)')
plt.ylabel('Number of\nAgents', rotation = 0)
ax.yaxis.set_label_coords(-0.2, 0.5)
plt.title("Number of Agents Categorized by Type")
plt.legend()
plt.savefig('outputs/agent_counts.png', dpi = 600)
plt.show()

# # #counts of oysters and shells
# # pops = results_df.groupby(['Step', 'mort_cause']).size().reset_index(name='counts')
# # sns.lineplot(data=pops, x='Step', y='counts', hue='mort_cause')
# # plt.xlabel('step')
# # plt.legend()
# # plt.show()

# # #get oyster ages
# oyster_all = results_df[results_df.type == "Oyster"]
# means = oyster_all.groupby('Step').mean("energy")
# plt.plot((means.energy), label = "energy")
# plt.xlabel('step')
# plt.legend()
# plt.show()

# # # means = iteration_one.groupby('Step').mean("shell_length_mm")
# # # plt.plot((means.shell_length_mm), label = "mean shell length")
# # # plt.xlabel('step')
# # # plt.legend()
# # # plt.show()

# # #first filter the results for one iteration one agent to look at oyster metrics
# oyster_one = results_df[(results_df.AgentID == "oyster_1094")]

# # #plot things (Oyster)
# plt.plot(oyster_one.Step, oyster_one.shell_length_mm, label = "shell_length_mmt")
# plt.show()


# #plt.plot(results_df.Step, results_df.alive, label = "alive")
# plt.plot(results_df.Step, results_df.no_energy, label = "no energy")
# plt.plot(results_df.Step, results_df.old_age, label = "old age")
# plt.plot(results_df.Step, results_df.no_energy_eight_days, label = "no energy for 8 days")
# plt.plot(results_df.Step, results_df.mortality, label = "mort prob")
# plt.plot(results_df.Step, results_df.out_of_water, label = "out of water")
# plt.legend()
# plt.title('cause of death')
# plt.show()
# #plt.plot(iteration_one.Step, iteration_one.wet_biomass, label = "wet_biomass")
# # #plt.plot(iteration_one.Step, iteration_one.shell_length_mm, label = "shell length (mm)")
# # #plt.plot(iteration_one.Step, iteration_one.energy, label = "energy")
# # #plt.plot(iteration_one.Step, iteration_one.fertility, label = "fertility")
# # #plt.plot(iteration_one.Step, iteration_one.mortality_prob, label = "mortality prob")


