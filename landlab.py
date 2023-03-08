#import libraries
from pylab import show, figure

import numpy as np
import matplotlib.pyplot as plt

#import mesa model
from model import *
from agents import *

#store model
oys_mod = OysterModel(500, 0, 0)

def generate_reef_map(model):
    reef_map = np.zeros((model.space.raster_layer.width, model.space.raster_layer.height))
    for cell in model.space.raster_layer:
        cell_content, x, y = cell
        for agent in cell_content:
            if type(agent) is Oyster:
                reef_map[x][y] = 2
            elif type(agent) is Shell:
                reef_map[x][y] = 1
    return reef_map

def plot_reef_map(reef_map):  
    plt.imshow(reef_map, interpolation='nearest')
    plt.colorbar()

oys_mod.run_model(step_count=20)
gm = generate_reef_map(oys_mod)
plot_reef_map(gm)


# #import raster
# (mg, z) = read_esri_ascii("oyster_dem_1.asc", name = "topographic_elevation")
# mg.at_node.keys()

# #plot raster
# figure('Elevations from the field')  # new fig, with a name
# imshow_grid_at_node(mg, "topographic_elevation")
# show()

# #run tidal flow calculator
# tfc = TidalFlowCalculator(mg, tidal_range=2.0, tidal_period=4.0e4, roughness=0.01)
# tfc.run_one_step()

# #get innudiation rate
# period = 4.0e4  # tidal period in s, for convenient calculation
# tfc = TidalFlowCalculator(mg, tidal_period=period)
# rate = tfc.calc_tidal_inundation_rate()
# mg = 0.5 * rate["topographic_elevation"] * period # depth in m
# mg.at_node.keys()

# #water depth ()
# figure('water depth')  # new fig, with a name
# imshow_grid_at_node(mg, 'mean_water__depth')
# show()