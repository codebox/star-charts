# -*- coding: utf-8 -*-
from __future__ import division
from math import sin, cos, degrees, radians, pi

'''
class RaDec:
    def __init__(self, ra, dec):
        self.ra  = ra
        self.dec = dec

    def _ra_to_angle(self, ra):
        # convert right-ascension (0 -> 24) into angle (0 -> 2π)
        return pi * 2 * (1 - ra / 24)

    def _dec_to_angle(self, dec):
        # convert declination (-90 -> +90) into angle (-π/2 -> +π/2)
        return radians(dec)

    def to_angle_pair(self):
        ra_angle  = pi * 2 * (1 - self.ra / 24)
        dec_angle = radians(self.dec)
        return AnglePair(ra_angle, dec_angle)

class AnglePair:
    def __init__(self, ra_angle, dec_angle):
        self.ra_angle  = ra_angle
        self.dec_angle = dec_angle

    def to_xy(self, center):
        # http://www.projectpluto.com/project.htm
        delta_ra = self.ra_angle - center.ra_angle
        x = cos(self.dec_angle) * sin(delta_ra)
        y = sin(self.dec_angle) * cos(center.dec_angle) - cos(self.dec_angle) * cos(delta_ra) * sin(center.dec_angle)
        return XYCoord(x,y)

class XYCoord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def offset_and_scale(self, x_offset, y_offset, scale):
        new_x = (self.x + x_offset) * scale
        new_y = (self.y + y_offset) * scale

        return XYCoord(new_x, new_y)


class XYCoords:
    def __init__(self, xy_coords):
        self.min_x = min(map(lambda xy : xy.x, xy_coords))
        self.min_y = min(map(lambda xy : xy.y, xy_coords))
        self.max_x = max(map(lambda xy : xy.x, xy_coords))
        self.max_y = max(map(lambda xy : xy.y, xy_coords))
        self.coords = xy_coords

    def offset_and_scale(self, diagram_size):
        x_range = self.max_x - self.min_x
        y_range = self.max_y - self.min_y
        max_range = max(x_range, y_range)

        magnification = diagram_size / max_range

        new_xy_coords = map(lambda xy: xy.offset_and_scale(self.min_x, self.min_y, magnification), self.coords)
        return XYCoords(new_xy_coords)
'''

class CoordCalc:
    def __init__(self, star_data_list, area, diagram_size):
        self.star_data_list = star_data_list
        self.center_ra_angle  = self._ra_to_angle((area.ra_min + area.ra_max)/2)
        self.center_dec_angle = self._dec_to_angle((area.dec_min + area.dec_max)/2)
        self.diagram_size = diagram_size

    def _ra_to_angle(self, ra):
        # convert right-ascension (0 -> 24) into angle (0 -> 2π)
        return pi * 2 * (1 - ra / 24)

    def _dec_to_angle(self, dec):
        # convert declination (-90 -> +90) into angle (-π/2 -> +π/2)
        return radians(dec)

    def _populate_angles(self):
        for star_data in self.star_data_list.data:
            star_data.ra_angle  = self._ra_to_angle(star_data.ra)
            star_data.dec_angle = self._dec_to_angle(star_data.dec)

    def _populate_xy(self):
        for star_data in self.star_data_list.data:
            # http://www.projectpluto.com/project.htm
            delta_ra = star_data.ra_angle - self.center_ra_angle
            star_data.x = cos(star_data.dec_angle) * sin(delta_ra)
            star_data.y = sin(star_data.dec_angle) * cos(self.center_dec_angle) - cos(star_data.dec_angle) * cos(delta_ra) * sin(self.center_dec_angle)

    def _offset_and_scale_xy(self):
        min_x = min(map(lambda sd : sd.x, self.star_data_list.data))
        min_y = min(map(lambda sd : sd.y, self.star_data_list.data))
        max_x = max(map(lambda sd : sd.x, self.star_data_list.data))
        max_y = max(map(lambda sd : sd.y, self.star_data_list.data))

        x_range = max_x - min_x
        y_range = max_y - min_y
        print x_range, y_range
        max_range = max(x_range, y_range)

        magnification = self.diagram_size / max_range
        print magnification

        def offset_and_scale_x(x):
            return (x - min_x) * magnification

        def offset_and_scale_y(y):
            return (y - min_y) * magnification

        def offset_and_scale(star_data):
            star_data.x = offset_and_scale_x(star_data.x)
            star_data.y = offset_and_scale_y(star_data.y)

        self.star_data_list.min_x = offset_and_scale_x(min_x)
        self.star_data_list.min_y = offset_and_scale_y(min_y)
        self.star_data_list.max_x = offset_and_scale_x(max_x)
        self.star_data_list.max_y = offset_and_scale_y(max_y)

        for star_data in self.star_data_list.data:
            print "({},{}) -> ({},{}) -> ({},{})".format(star_data.ra, star_data.dec, star_data.ra_angle, star_data.dec_angle, star_data.x, star_data.y)
            offset_and_scale(star_data)

    def process(self):
        self._populate_angles()
        self._populate_xy()
        self._offset_and_scale_xy()
