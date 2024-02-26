import landlab
import numpy as np
import matplotlib as plt


(mg, z) = landlab.io.esri_ascii.read_esri_ascii("data/oyster_dem_filled.asc", name="topographic__elevation")


from landlab.plot.imshow import imshow_grid


imshow_grid(mg, "topographic__elevation")

np.flipud(mg)

from landlab.plot.graph import plot_graph
from landlab import RasterModelGrid

grid = RasterModelGrid((4, 5), xy_spacing=(10, 5))
plot_graph(grid, at="node")




