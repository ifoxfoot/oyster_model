from landlab import RasterModelGrid
from landlab.components import TidalFlowCalculator
from landlab.plot import imshow
from pylab import show, figure

#make raster data
grid = RasterModelGrid((3, 5), xy_spacing=2.0) 
z = grid.add_zeros("topographic__elevation", at = "node")
z[5:10] = [2.0, 0.25, 0.0, -0.25, -3.0]

#plot raster
figure('Elevations from the field')  # new fig, with a name
imshow.imshow_grid_at_node(grid, "topographic__elevation")
show()


tfc = TidalFlowCalculator(grid, tidal_range=1.289919, tidal_period=43482.58, roughness=0.05)

#run the tidal flow calc
tfc.run_one_step()

names = tfc.output_var_names

#store tidal period for depth
period=4.0e4

#get innudiation rate
rate = tfc.calc_tidal_inundation_rate()

#get high tide water level
dem_high = 1 * period * rate[:]  # depth in m
grid.add_field("water_high", dem_high, at = "node")

#get low tide water level
dem_low = 0.5 * rate[:] * period # depth in m
grid.add_field("water_low", dem_low, at = "node")

depth = grid.add_field("water_depth", tfc._water_depth, at = "node")

m_depth = grid.add_field("mean_water_depth", tfc., at = "node")

#water depth ()
figure('water depth (tfc_output)')  # new fig, with a name
imshow.imshow_grid_at_node(grid = grid, values = 'water_depth', limits = (0,4))
show()

#water depth ()
figure('water depth (low tide)')  # new fig, with a name
imshow.imshow_grid_at_node(grid = grid, values = 'water_low', limits = (0,4))
show()

#water depth ()
figure('water depth (high tide)')  # new fig, with a name
imshow.imshow_grid_at_node(grid = grid, values = 'water_high', limits = (0,4))
show()

shell_length_mm = 300
dry_biomass = 9.6318 * (10**-6) * (shell_length_mm**2.743)
wet_biomass =  (dry_biomass * 5.6667) + dry_biomass
shell_weight = wet_biomass * 3.4

