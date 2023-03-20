
#make raster data
import numpy as np

x = np.linspace(-90, 90, 6)
y = np.linspace(90, -90, 6)
X, Y = np.meshgrid(x, y)
Z1 =  np.abs(((X - 10) ** 2 + (Y - 10) ** 2) / 1 ** 2)
Z2 =  np.abs(((X + 10) ** 2 + (Y + 10) ** 2) / 2.5 ** 2)
Z =  (Z1 - Z2)

#write to raster

from rasterio.transform import Affine

xres = (x[-1] - x[0]) / len(x)
yres = (y[-1] - y[0]) / len(y)

transform = Affine.translation(x[0] - xres / 2, y[0] - yres / 2) * Affine.scale(xres, yres)

with rasterio.open(
        "data/temperature.tif",
        mode="w",
        driver="GTiff",
        height=Z.shape[0],
        width=Z.shape[1],
        count=1,
        dtype=Z.dtype,
        crs="+proj=latlong",
        transform=transform,
) as new_dataset:
        new_dataset.write(Z, 1)

import rasterio
#open it
raster = rasterio.open("data/oyster_dem_buf.asc")


from landlab import RasterModelGrid
from landlab.io import read_esri_ascii

#create raster model grid
rmg = RasterModelGrid((raster.height, raster.width))
#add data from grid
rmg.add_field("temp", raster.read(1), at = "node")

from landlab.plot.imshow import imshow_grid_at_node
from pylab import show, figure

imshow_grid_at_node(rmg, "temp")
show()
