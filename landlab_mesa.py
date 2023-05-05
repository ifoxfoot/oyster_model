#import libraries
from landlab.plot import imshow
from pylab import show, figure
from landlab.components import TidalFlowCalculator
from landlab import RasterModelGrid
from landlab.io.esri_ascii import write_esri_ascii
import os
import matplotlib.pyplot as plt
from numpy import flip

#import mesa model
from model import *
from space import *
from agents import *

#store model
oys_mod = OysterModel()

oys_mod.run_model(steps = 365*5)

rmg = RasterModelGrid((oys_mod.space.raster_layer.height, 
                       oys_mod.space.raster_layer.width),
                       1.157226984026
                       )
rmg.add_field("topographic__elevation", 
              np.fliplr(oys_mod.space.raster_layer.get_raster("elevation")))
rmg.add_field("num_oysters",
              np.fliplr(oys_mod.space.raster_layer.get_raster("num_oysters_in_cell")))

#plot raster
figure('num oysters from the model')  # new fig, with a name
imshow.imshow_grid_at_node(rmg, "num_oysters")
# ax = plt.gca()
# ax.set_ylim(ax.get_ylim()[::-1])
show()

#store roughness values
rough = rmg.add_zeros("node", 'mannings_n')
sand_roughness = 0.02
oyster_roughness = 0.035

#store roughness vals in attribute of rastermodel grid
rough[rmg.at_node["num_oysters"] == 0] = sand_roughness
rough[rmg.at_node["num_oysters"] > 0] = oyster_roughness

#plot raster
figure('Roughness vals')  # new fig, with a name
imshow.imshow_grid_at_node(rmg, "mannings_n")
# ax = plt.gca()
# ax.set_ylim(ax.get_ylim()[::-1])
show()

#map roughness to link
r_link = rmg.map_mean_of_link_nodes_to_link("mannings_n")

#init tidal flow calculator
tfc = TidalFlowCalculator(rmg, tidal_range = 1.289919, tidal_period = 43482.58, roughness = r_link)

#run it
tfc.run_one_step()

#convert flow back to nodes
ebb_vel = rmg.map_max_of_node_links_to_node("ebb_tide_flow__velocity")
rmg.add_field("ebb_vel", ebb_vel)

flood_vel = rmg.map_max_of_node_links_to_node("flood_tide_flow__velocity")
rmg.add_field("flood_vel", flood_vel)

#plot raster
figure('Tidal Flow Ebb')  # new fig, with a name
imshow.imshow_grid_at_node(rmg, "ebb_vel")
# ax = plt.gca()
# ax.set_ylim(ax.get_ylim()[::-1])
show()

#plot raster
figure('Tidal Flow Flood')  # new fig, with a name
imshow.imshow_grid_at_node(rmg, "ebb_vel")
# ax = plt.gca()
# ax.set_ylim(ax.get_ylim()[::-1])
show()

#write to raster
files = write_esri_ascii("outputs/five_years.asc", rmg)
[os.path.basename(name) for name in sorted(files)]