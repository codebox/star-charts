class StarData:
    def __init__(self, ra, dec, mag, label=None):
        self.ra    = ra
        self.dec   = dec
        self.mag   = mag
        self.label = label

        self.ra_angle  = None
        self.dec_angle = None

        self.x = None
        self.y = None

class StarDataList:
    def __init__(self, data):
        self.data = data
        self.min_x = self.max_x = self.min_y = self.max_y = None