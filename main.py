
import sky_area
from input_file import InputFile
from diagram import Diagram
from coord_calc import CoordCalc

f = InputFile('stardata.csv')

area = sky_area.SKY_AREA_ORION
star_data_list = f.get_stars(area)

cc = CoordCalc(star_data_list, area, 500)
cc.process()

d = Diagram('My Star Map', area, star_data_list)
list(map(d.add_curve, cc.calc_curves()))
d.render_svg('star-chart.svg')
