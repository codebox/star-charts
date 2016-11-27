from __future__ import division
import sky_area
from input_file import InputFile
from diagram import Diagram
from coord_calc import CoordCalc

f = InputFile('stardata/in.csv')

area = sky_area.SKY_AREA_ORION
star_data_list = f.get_stars(area)

CoordCalc(star_data_list, area, 500).process()

d = Diagram('My Star Map', area, star_data_list)
d.render_svg('star-chart.svg')
