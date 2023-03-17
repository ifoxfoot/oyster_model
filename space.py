#import required libraries
import mesa
import mesa_geo as mg
import numpy as np
import rasterio as rio

#class for cells in raster
class SeaBedCell(mg.Cell):
    elevation: int | None
    num_oysters_in_cell: int | None

    def __init__(
        self,
        pos: mesa.space.Coordinate | None = None,
        indices: mesa.space.Coordinate | None = None,
    ):
        super().__init__(pos, indices)
        self.elevation = None
        self.num_oysters_in_cell = None

    def step(self):
        pass

#set up class for space
class SeaBed(mg.GeoSpace):
    def __init__(self, crs):
        super().__init__(crs = crs)

    #read in raster layer
    def set_elevation_layer(self, crs):
        raster_layer = mg.RasterLayer.from_file(
            "data/oyster_dem_buf.asc", 
            cell_cls = SeaBedCell, 
            attr_name = "elevation"
            )
        raster_layer.crs = crs
        raster_layer.apply_raster(
            data = np.zeros(shape = (1, raster_layer.height, raster_layer.width)),
            attr_name = "num_oysters_in_cell",
        )
        #add raster layer
        super().add_layer(raster_layer)

    #return raster layer when called
    @property
    def raster_layer(self):
        return self.layers[0]
    
    #when an oyster is added, add it to raster layer
    def add_oyster(self, oyster):
        row, col = rio.transform.rowcol(
            self.raster_layer.transform, 
            oyster.geometry.x, oyster.geometry.y)
        x = col
        y = row - self.raster_layer.height -1
        self.raster_layer.cells[x][-y].num_oysters_in_cell += 1
    

