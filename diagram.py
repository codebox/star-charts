from __future__ import division
from svg import Svg
import codecs

MARGIN=20
MAGNIFICATION = 500

MIN_D = 1
MAX_D = 4

DIMMEST_MAG = 6
BRIGHTEST_MAG = -1.5

LABEL_OFFSET_X = 4
LABEL_OFFSET_Y = 3
FONT_SIZE=16
FONT_COLOUR='#167ac6'

STAR_COLOUR='#000'

CURVE_WIDTH = 0.1
CURVE_COLOUR = '#000'

class Diagram:
    def __init__(self):
        self.points = []
        self.curves = []
        self.border_min_x = self.border_min_y = self.border_max_x = self.border_max_y = None

    def add_point(self, x, y, m, l):
        self.points.append((x, y, m, l))

    def add_curve(self, curve_points):
        self.curves.append(curve_points)

    def _mag_to_d(self, m):
        mag_range = DIMMEST_MAG - BRIGHTEST_MAG
        m_score = (DIMMEST_MAG - m) / mag_range
        r_range = MAX_D - MIN_D
        return MIN_D + m_score * r_range

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

    def render_svg(self, outfile):
        svg = Svg()

        normalised_coords = self._normalise_coords()

        # add stars first
        for point in normalised_coords:
            _x, _y, m, _ = point
            d = self._mag_to_d(m)
            x = MARGIN + _x * MAGNIFICATION
            y = MARGIN + _y * MAGNIFICATION

            svg.circle(x, y, d, STAR_COLOUR)

        # next add labels
        for point in self._normalise_coords():
            _x, _y, m, l = point

            if l:
                d = self._mag_to_d(m)
                x = MARGIN + _x * MAGNIFICATION
                y = MARGIN + _y * MAGNIFICATION
                svg.text(x + LABEL_OFFSET_X + d/2, y + LABEL_OFFSET_Y, l, FONT_COLOUR, FONT_SIZE)

        # next add curves
        for curve_points in self.curves:
            normalised_curve_points = []
            for cp in curve_points:
                ccx, ccy = self._convert_coord(cp[0], cp[1])
                normalised_curve_points.append((MARGIN + ccx * MAGNIFICATION, MARGIN + ccy * MAGNIFICATION))

            svg.curve(normalised_curve_points, CURVE_WIDTH, CURVE_COLOUR)

        codecs.open(outfile, 'w', 'utf-8').writelines(svg.to_list())
