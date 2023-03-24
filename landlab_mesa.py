#import libraries
from rasterio.plot import show as showr
from landlab.plot import imshow
from landlab.io import read_esri_ascii
from pylab import show, figure
from landlab.components import TidalFlowCalculator
import matplotlib.pyplot as plt
from landlab import RasterModelGrid
import numpy as np

#import mesa model
from model import *
from space import *
from agents import *

#store model
oys_mod = OysterModel(500, 0, 0)


rmg = RasterModelGrid((oys_mod.space.raster_layer.height, 
                       oys_mod.space.raster_layer.width),
                       1.157226984026, 
                       (-9051628.873678505, 3492744.042225802))
rmg.add_field("topographic__elevation", 
              oys_mod.space.raster_layer.get_raster("elevation"))
rmg.add_field("num_oysters",
              oys_mod.space.raster_layer.get_raster("num_oysters_in_cell"))

#plot raster
figure('Elevations from the field')  # new fig, with a name
imshow.imshow_grid_at_node(rmg, "topographic__elevation")
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
show()

#map roughness to link
r_link = rmg.map_max_of_link_nodes_to_link("mannings_n")
rough_two = rmg.add_field("rough_link", r_link, at = "link")

#init tidal flow calculator
tfc = TidalFlowCalculator(rmg, tidal_range = 2.0, tidal_period = 4.0e4, roughness = rough_two)

#run the tidal flow calc
for i in range(50):
    tfc.run_one_step()

#store tidal period for depth
period=4.0e4

#get innudiation rate
rate = tfc.calc_tidal_inundation_rate()
depth = 0.5 * rate[:] * period # depth in m
rmg.add_field("water", depth, at = "node")

#water depth ()
figure('water depth')  # new fig, with a name
imshow.imshow_grid_at_node(rmg, 'water')
show()

