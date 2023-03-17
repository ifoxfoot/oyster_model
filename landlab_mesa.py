#import libraries
from rasterio.plot import show as showr
from landlab.plot import imshow
from landlab.io import read_esri_ascii
from pylab import show, figure
from landlab.components import TidalFlowCalculator
import matplotlib.pyplot as plt
from landlab import RasterModelGrid, imshow_grid

#import mesa model
from model import *
from space import *
from agents import *

#store model
oys_mod = OysterModel(500, 0, 0)

#fun to generate reeef map
def generate_reef_map(model):
    raster = oys_mod.space.raster_layer.get_raster("num_oysters_in_cell")
    return(raster)

#fun to plot reef map
def plot_reef_map(reef_map):  
    showr(reef_map)

#test out funs
oys_mod.run_model(step_count=20)
map = generate_reef_map(oys_mod)
plot_reef_map(map)

rmg = RasterModelGrid((oys_mod.space.raster_layer.width, oys_mod.space.raster_layer.height))

#import raster
(dem, z) = read_esri_ascii("data/oyster_dem_buf.asc", name = "topographic__elevation")
dem.at_node.keys()

#plot raster
figure('Elevations from the field')  # new fig, with a name
imshow.imshow_grid_at_node(dem, "topographic__elevation")
show()

#store roughness values
rough = dem.add_zeros('mannings_n', at='node')
sand_roughness = 0.02
oyster_roughness = 0.035

#store roughness vals in attribute of rastermodel grid
rough[map.flatten()>0] = sand_roughness
rough[map.flatten()==0] = oyster_roughness

# tidal period in s, for convenient calculation
period = 4.0e4

#init tidal flow calculator
tfc = TidalFlowCalculator(dem, tidal_range=2.0, tidal_period=4.0e4, roughness=rough)

#run the tidal flow calc
for i in range(50):
    tfc.run_one_step()

#get innudiation rate
rate = tfc.calc_tidal_inundation_rate()
dem = 0.5 * rate["topographic__elevation"] * period # depth in m
dem.at_node.keys()

#water depth ()
figure('water depth')  # new fig, with a name
imshow_grid.imshow_grid_at_node(dem, 'mean_water__depth')
show()

