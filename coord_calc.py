# -*- coding: utf-8 -*-

from math import sin, cos, degrees, radians, pi

class CoordCalc:
    def __init__(self, star_data_list, area, diagram_size):
        self.star_data_list = star_data_list
        self.area = area
        self.center_ra_angle  = self._ra_to_angle((area.ra_min + area.ra_max)/2)
        if area.ra_max - area.ra_min >= 12:
            self.center_dec_angle = self._dec_to_angle(90 if abs(area.dec_min) < abs(area.dec_max) else -90)
        else:
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

    def _angle_to_xy(self, ra_angle, dec_angle):
        # http://www.projectpluto.com/project.htm
        delta_ra = ra_angle - self.center_ra_angle
        x = cos(dec_angle) * sin(delta_ra)
        y = sin(dec_angle) * cos(self.center_dec_angle) - cos(dec_angle) * cos(delta_ra) * sin(self.center_dec_angle)
        return x,y

    def _populate_xy(self):
        for star_data in self.star_data_list.data:
            star_data.x, star_data.y = self._angle_to_xy(star_data.ra_angle, star_data.dec_angle)

    def _offset_and_scale_xy(self):
        min_x = min([sd.x for sd in self.star_data_list.data])
        min_y = min([sd.y for sd in self.star_data_list.data])
        max_x = max([sd.x for sd in self.star_data_list.data])
        max_y = max([sd.y for sd in self.star_data_list.data])

        x_range = max_x - min_x
        y_range = max_y - min_y
        max_range = max(x_range, y_range)

        self.magnification = self.diagram_size / max_range

        def offset_and_scale_x(x):
            return (x - min_x) * self.magnification

        def offset_and_scale_y(y):
            return (y - min_y) * self.magnification

        def offset_and_scale(star_data):
            star_data.x = offset_and_scale_x(star_data.x)
            star_data.y = offset_and_scale_y(star_data.y)

        self.star_data_list.min_x = offset_and_scale_x(min_x)
        self.star_data_list.min_y = offset_and_scale_y(min_y)
        self.star_data_list.max_x = offset_and_scale_x(max_x)
        self.star_data_list.max_y = offset_and_scale_y(max_y)
        self.offset_and_scale_x = offset_and_scale_x
        self.offset_and_scale_y = offset_and_scale_y

        list(map(offset_and_scale, self.star_data_list.data))

    def process(self):
        self._populate_angles()
        self._populate_xy()
        self._offset_and_scale_xy()

    def _ra_dec_to_x_y(self, ra, dec):
        ra_angle  = self._ra_to_angle(ra)
        dec_angle = self._dec_to_angle(dec)

        base_x, base_y = self._angle_to_xy(ra_angle, dec_angle)

        return self.offset_and_scale_x(base_x), self.offset_and_scale_y(base_y)

    def calc_ra_curve(self, ra, steps):
        points = []
        dec_min = self.area.dec_min
        dec_max = self.area.dec_max
        dec_step =  (dec_max - dec_min) / steps

        for i in range(steps+1):
            x, y = self._ra_dec_to_x_y(ra, dec_min + dec_step * i)
            points.append((x, y))

        return points

    def calc_dec_curve(self, dec, steps):
        points = []
        ra_min = self.area.ra_min
        ra_max = self.area.ra_max
        ra_step =  (ra_max - ra_min) / steps

        for i in range(steps+1):
            x, y = self._ra_dec_to_x_y(ra_min + ra_step * i, dec)
            points.append((x,y))

        return points

    def calc_curves(self, ra_steps=100, dec_steps=100):
        curves = []

        curves.append(self.calc_ra_curve(self.area.ra_min, ra_steps))
        ra = round(self.area.ra_min)
        while ra < self.area.ra_max:
            if ra > self.area.ra_min:
                curves.append(self.calc_ra_curve(ra, ra_steps))
            ra += 1
        curves.append(self.calc_ra_curve(self.area.ra_max, ra_steps))

        curves.append(self.calc_dec_curve(self.area.dec_min, dec_steps))
        dec = round(self.area.dec_min / 10) * 10
        while dec < self.area.dec_max:
            if dec > self.area.dec_min:
                curves.append(self.calc_dec_curve(dec, dec_steps))
            dec += 10
        curves.append(self.calc_dec_curve(self.area.dec_max, dec_steps))

        return curves
