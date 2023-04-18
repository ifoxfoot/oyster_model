#import required libraries
import mesa
import mesa_geo as mg
import numpy as np


#class for cells in raster
class SeaBedCell(mg.Cell):
    elevation: int | None
    num_oysters_in_cell: int | None
    water_level: float | None

    def __init__(
        self,
        pos: mesa.space.Coordinate | None = None,
        indices: mesa.space.Coordinate | None = None,
    ):
        super().__init__(pos, indices)
        self.elevation = None
        self.num_oysters_in_cell = None
        self.water_level = None

    def step(self):
        pass

#set up class for space
class SeaBed(mg.GeoSpace):
    def __init__(self, crs):
        super().__init__(crs = crs)

    #read in raster layer
    def set_elevation_layer(self, crs):
        raster_layer = mg.RasterLayer.from_file(
            "data/oyster_dem_filled.asc", 
            cell_cls = SeaBedCell, 
            attr_name = "elevation"
            )
        raster_layer.crs = crs
        raster_layer.apply_raster(
            data = np.zeros(shape = (1, raster_layer.height, raster_layer.width)),
            attr_name = "num_oysters_in_cell",
        )
        super().add_layer(raster_layer)

    #return raster layer when called
    @property
    def raster_layer(self):
        return self.layers[0]
    
    #when an oyster is added, add it to raster layer
    def add_oyster(self, oyster):
        self.raster_layer.cells[oyster.x][-oyster.y].num_oysters_in_cell += 1

    #when an oyster is added, add it to raster layer
    def remove_oyster(self, oyster):
        self.raster_layer.cells[oyster.x][-oyster.y].num_oysters_in_cell -= 1
    

