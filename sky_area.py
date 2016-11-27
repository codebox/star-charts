class SkyArea:
    def __init__(self, ra0, ra1, dec0, dec1, mag_min):
        self.ra_min  = min(ra0, ra1)
        self.ra_max  = max(ra0, ra1)
        self.dec_min = min(dec0, dec1)
        self.dec_max = max(dec0, dec1)
        self.mag_min = mag_min

SKY_AREA_ORION  = SkyArea(5, 6, -10, 10, 8)
SKY_AREA_TAURUS = SkyArea(4, 6, 10, 30, 6)
SKY_AREA_NORTH = SkyArea(0, 20, 0, 60, 6)
