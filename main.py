from __future__ import division
import sky_area
from input_file import InputFile
from diagram import Diagram
from coord_calc import CoordCalc

f = InputFile('stardata/in.csv')

area = sky_area.SKY_AREA_NORTH
star_data_list = f.get_stars(area)

cc = CoordCalc(star_data_list, area, 500)
cc.process()

d = Diagram('My Star Map', area, star_data_list)
map(d.add_curve, cc.calc_curves())
d.render_svg('star-chart.svg')
