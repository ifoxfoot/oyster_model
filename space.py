#import required libraries
import mesa
import mesa_geo as mg
import numpy as np


#class for cells in raster
class SeaBedCell(mg.Cell):
    elevation: int | None
    population: int | None

    def __init__(
        self,
        pos: mesa.space.Coordinate | None = None,
        indices: mesa.space.Coordinate | None = None,
    ):
        super().__init__(pos, indices)
        self.elevation = None
        self.population = None

    def step(self):
        pass


#set up class for space
class SeaBed(mg.GeoSpace):
    def __init__(self, crs):
        super().__init__(crs = crs)

    def set_elevation_layer(self, crs):
        raster_layer = mg.RasterLayer.from_file(
            "data/oyster_dem.tif", 
            cell_cls = SeaBedCell, 
            attr_name = "elevation"
            )
        raster_layer.crs = crs
        raster_layer.apply_raster(
            data = np.ones(shape = (1, raster_layer.height, raster_layer.width)),
            attr_name = "elevation",
        )
        super().add_layer(raster_layer)

    @property
    def raster_layer(self):
        return self.layers[0]
    

