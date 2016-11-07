from __future__ import division
from math import sin, cos, degrees, radians, pi
from input_file import InputFile
from diagram import Diagram

IN_FILE = 'stardata/in.csv'
MIN_MAG=10

'''
#Ursa-Major
RA_RANGE=(11, 14)
DEC_RANGE=(45, 65)

# Orion
RA_RANGE=(5, 6)
DEC_RANGE=(-10, 10)

#Ursa-Minor
RA_RANGE=(0, 24)
DEC_RANGE=(-90, 0)

RA_RANGE=(4, 6)
DEC_RANGE=(10, 30)
'''
# Orion
RA_RANGE=(5, 6)
DEC_RANGE=(-10, 10)

RA_STEP=1
DEC_STEP=10

def _calc(ra0, dec0, ra, dec):
    # http://www.projectpluto.com/project.htm
    delta_ra = ra - ra0;
    x1 = cos(dec) * sin(delta_ra)
    y1 = sin(dec) * cos(dec0) - cos(dec) * cos(delta_ra) * sin(dec0)
    return x1, y1

def _ra_to_angle(ra):
    return pi * 2 * (1 - ra / 24)

def _dec_to_angle(dec):
    return radians(dec)

# expects ra: 0 -> 24, dec: +90 -> -90
def calc(ra, dec):
    centre_ra  = sum(RA_RANGE) / 2 #TODO this isn't quite right, eg RA of (0,24) it should center on 0 not 12
    centre_dec = sum(DEC_RANGE) / 2
    return _calc(_ra_to_angle(centre_ra), _dec_to_angle(centre_dec), _ra_to_angle(ra), _dec_to_angle(dec))

f = InputFile(IN_FILE)

d = Diagram()

for s in f.get_stars(RA_RANGE, DEC_RANGE, MIN_MAG):
    ra, dec, mag, l = s
    x,y = calc(ra, dec)
    d.add_point(x, y, mag, l)

def add_ra_dec_curves(d, min_ra, max_ra, ra_step, min_dec, max_dec, dec_step):
    first_ra_line  = min_ra if min_ra % ra_step == 0 else min_ra + ra_step - min_ra % ra_step
    last_ra_line   = max_ra if max_ra % ra_step == 0 else max_ra - max_ra % ra_step
    first_dec_line = min_dec if min_dec % dec_step == 0 else min_dec + dec_step - min_dec % dec_step
    last_dec_line  = max_dec if max_dec % dec_step == 0 else max_dec - max_dec % dec_step

    ra_lines = []
    ra = first_ra_line
    while ra < last_ra_line:
        ra_lines.append(ra)
        ra += ra_step
    ra_lines.append(last_ra_line)

    dec_lines = []
    dec = first_dec_line
    while dec < last_dec_line:
        dec_lines.append(dec)
        dec += dec_step
    dec_lines.append(last_dec_line)

    #TODO need more points on curves to make shape better
    for ra in ra_lines:
        p = [calc(ra, min_dec)]
        for dec in dec_lines:
            p.append(calc(ra, dec))
        p.append(calc(ra, max_dec))

        d.add_curve(p)

    for dec in dec_lines:
        p = [calc(min_ra, dec)]
        for ra in ra_lines:
            p.append(calc(ra, dec))
        p.append(calc(max_ra, dec))

        d.add_curve(p)


add_ra_dec_curves(d, RA_RANGE[0], RA_RANGE[1], RA_STEP, DEC_RANGE[0], DEC_RANGE[1], DEC_STEP)

d.render_svg('star-chart.svg')
