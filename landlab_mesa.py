#import librariesf
from rasterio.plot import show
from landlab import RasterModelGrid, imshow_grid
from landlab.io import read_esri_ascii
import matplotlib.pyplot as plt

#import mesa model
from model import *
from space import *
from agents import *

#store model
oys_mod = OysterModel(500, 0, 0)

#store roughness values
sand_roughness = 0.02
oyster_roughness = 0.035


def generate_reef_map(model):
    raster = oys_mod.space.raster_layer.get_raster("num_oysters_in_cell")
    return(raster)

def plot_reef_map(reef_map):  
    show(reef_map)
  
oys_mod.run_model(step_count=20)
map = generate_reef_map(oys_mod)
plot_reef_map(map)


#import raster
(dem, z) = read_esri_ascii("data/oyster_dem_1.asc.gz", name = "topographic_elevation")
dem.at_node.keys()

#plot raster
imshow_grid.figure('Elevations from the field')  # new fig, with a name
imshow_grid.imshow_grid_at_node(mg, "topographic_elevation")
imshow_grid.show()

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