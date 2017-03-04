class SkyArea:
    def __init__(self, ra0, ra1, dec0, dec1, mag_min):
        self.ra_min  = min(ra0, ra1)
        self.ra_max  = max(ra0, ra1)
        self.dec_min = min(dec0, dec1)
        self.dec_max = max(dec0, dec1)
        self.mag_min = mag_min

SKY_AREA_ORION  = SkyArea(4.5, 6.5, -15, 15, 8)
SKY_AREA_TAURUS = SkyArea(4, 6, 10, 30, 8)
SKY_AREA_NORTH = SkyArea(0, 24, 50, 90, 7)
SKY_AREA_SOUTH = SkyArea(0, 24, -50, -90, 7)
SKY_AREA_URSA_MINOR = SkyArea(14, 18, 60, 90, 9)
