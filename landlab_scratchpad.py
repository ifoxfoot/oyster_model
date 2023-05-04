from landlab.io import read_esri_ascii
import numpy as np

(mg, z) = read_esri_ascii("data/oyster_dem_filled.asc", name="topographic__elevation")

from landlab.plot.imshow import imshow_grid


imshow_grid(mg, "topographic__elevation")

np.flipud(mg)