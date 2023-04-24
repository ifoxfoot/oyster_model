import numpy as np
import geopandas as gpd
from geopandas import overlay
from rasterio.features import rasterize
import rasterio 
from shapely.geometry import Polygon
import pandas as pd
import matplotlib.pyplot as plt

# # create a geopandas dataframe from the polygons and attributes
# # create a list of polygons
# polygons = [Polygon([(0, 0), (0, 1), (1, 1), (1, 0)]),
#             Polygon([(1, 1), (1, 2), (2, 2), (2, 1)]),
#             Polygon([(2, 2), (2, 3), (3, 3), (3, 2)])]

# # create a pandas dataframe with some attributes
# df = pd.DataFrame({'id': [1, 2, 3],
#                    'name': ['polygon 1', 'polygon 2', 'polygon 3'],
#                    'value': [10, 20, 30]})


# # create a geopandas dataframe from the polygons and attributes
# gdf = gpd.GeoDataFrame(df, geometry=polygons)
reef_data = gpd.read_file("data/oyster_reef_buf.gpkg")

#plot it
reef_data.plot("OBJECTID", legend = True)
plt.show()

selected_polygon = reef_data.loc[reef_data['OBJECTID'] == 7124]


# # Calculate the extent of the original geodataframe
# xmin, ymin, xmax, ymax = gdf.total_bounds

# # Create a bounding box polygon of the same extent as the original geodataframe
# bbox = Polygon([(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)])

# # Select a polygon and clip it to the extent of the original geodataframe
# selected_polygon = gdf[gdf['id'] == 1]
# clipped_polygon = selected_polygon.clip(bbox)

# #plot it
# clipped_polygon.plot()
# plt.show()

# specify the dimensions and resolution of your output raster
width = 259
height = 149
transform = rasterio.transform.from_bounds(*reef_data.total_bounds, width=width, height=height)

# create an empty raster to store the output
image = np.zeros((height, width), dtype=np.uint8)

# rasterize the polygons in the geodataframe and store the result in the output raster
shapes = ((geom, 255) for geom in selected_polygon.geometry)
ras = rasterize(shapes=shapes, out=image, transform=transform)

# plot rasterized
plt.imshow(ras)
plt.show()

