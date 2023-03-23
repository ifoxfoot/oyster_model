from landlab import RasterModelGrid
from landlab.components import TidalFlowCalculator
from landlab.plot import imshow
from pylab import show, figure


#make raster data
grid = RasterModelGrid((3, 4), xy_spacing=2.0) 
z = grid.add_zeros("topographic__elevation", at = "node")
z[1] = -50.0  # mean water depth is 50 m below MSL
rough = grid.add_zeros("roughness", at = "node")
rough[5] = 0.05

r_link = grid.calc_grad_at_link(rough)
rough_two = grid.add_field("rough_link", r_link, at = "link")

#plot raster
figure('Elevations from the field')  # new fig, with a name
imshow.imshow_grid_at_node(grid, "topographic__elevation")
show()

#plot raster
figure('Roughness vals')  # new fig, with a name
imshow.imshow_grid_at_node(grid, "roughness")
show()

tfc = TidalFlowCalculator(grid, tidal_range=2.0, tidal_period=4.0e4, roughness=rough_two)

#run the tidal flow calc
for i in range(50):
    tfc.run_one_step()

#store tidal period for depth
period=4.0e4

#get innudiation rate
rate = tfc.calc_tidal_inundation_rate()
dem = 0.5 * rate[:] * period # depth in m
grid.add_field("water", dem, at = "node")

#water depth ()
figure('water depth')  # new fig, with a name
imshow.imshow_grid_at_node(grid, 'mean_water__depth')
show()
