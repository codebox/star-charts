from __future__ import division
from svg import Svg
import codecs

MARGIN_X=20
MARGIN_Y=60
MAGNIFICATION = 500

MIN_D = 1
MAX_D = 4

DIMMEST_MAG = 6
BRIGHTEST_MAG = -1.5

LABEL_OFFSET_X = 4
LABEL_OFFSET_Y = 3
FONT_SIZE=16
FONT_COLOUR='#167ac6'

TITLE_SIZE=16
TITLE_COLOUR='#000'
COORDS_SIZE=12
COORDS_COLOUR='#000'

STAR_COLOUR='#000'

CURVE_WIDTH = 0.1
CURVE_COLOUR = '#000'

class Diagram:
    def __init__(self, title, area, star_data_list):
        self.title = title
        self.area = area
        self.star_data_list = star_data_list
        self.curves = []
        self.border_min_x = self.border_min_y = self.border_max_x = self.border_max_y = None

    def add_curve(self, curve_points):
        self.curves.append(curve_points)

    def _mag_to_d(self, m):
        mag_range = DIMMEST_MAG - BRIGHTEST_MAG
        m_score = (DIMMEST_MAG - m) / mag_range
        r_range = MAX_D - MIN_D
        return MIN_D + m_score * r_range

    '''
    def _normalise_coords(self):
        self.min_x = min(map(lambda p: p[0], self.points))
        self.min_y = min(map(lambda p: p[1], self.points))
        self.max_x = max(map(lambda p: p[0], self.points))
        self.max_y = max(map(lambda p: p[1], self.points))

        range_x = self.max_x - self.min_x
        range_y = self.max_y - self.min_y

        self.largest_range = max(range_x, range_y)

        nc = []
        for p in self.points:
            x, y = self._convert_coord(p[0], p[1])
            nc.append((x, y, p[2], p[3]))
        return nc

    def _convert_coord(self, ra, dec):
        return (ra - self.min_x) / self.largest_range, (self.max_y - dec) / self.largest_range
    '''

    def _invert_and_offset(self, x, y):
        return x + MARGIN_X, (self.star_data_list.max_y - y) + MARGIN_Y

    def render_svg(self, outfile):
        svg = Svg()

        # add stars first
        for star_data in self.star_data_list.data:
            x, y = self._invert_and_offset(star_data.x, star_data.y)
            svg.circle(x, y, self._mag_to_d(star_data.mag), STAR_COLOUR)

        # next add labels
        for star_data in self.star_data_list.data:
            if star_data.label:
                x, y = self._invert_and_offset(star_data.x, star_data.y)
                d = self._mag_to_d(star_data.mag)
                svg.text(x + LABEL_OFFSET_X + d/2, y + LABEL_OFFSET_Y, star_data.label, FONT_COLOUR, FONT_SIZE)

        # next add curves
        for curve_points in self.curves:
            normalised_curve_points = []
            for cp in curve_points:
                ccx, ccy = self._convert_coord(cp[0], cp[1])
                normalised_curve_points.append((MARGIN_X + ccx * MAGNIFICATION, MARGIN_Y + ccy * MAGNIFICATION))

            svg.curve(normalised_curve_points, CURVE_WIDTH, CURVE_COLOUR)

        # title
        center_x = self.star_data_list.max_x/2 + MARGIN_X
        svg.text(center_x, MARGIN_Y/2, self.title, TITLE_COLOUR, TITLE_SIZE, 'middle', 'underline')

        # coords
        chart_bottom_y = self.star_data_list.max_y + MARGIN_Y
        svg.text(center_x, chart_bottom_y + MARGIN_Y/2, "Right Ascension: {}-{}".format(self.area.ra_min, self.area.ra_max), COORDS_COLOUR, COORDS_SIZE, 'middle')
        svg.text(center_x, chart_bottom_y + MARGIN_Y/2 + COORDS_SIZE, "Declination: {}-{}".format(self.area.dec_min, self.area.dec_max), COORDS_COLOUR, COORDS_SIZE, 'middle')

        codecs.open(outfile, 'w', 'utf-8').writelines(svg.to_list())
