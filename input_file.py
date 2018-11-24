import codecs
from star_data import StarData, StarDataList

class InputFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_stars(self, sky_area):
        """
        Expected line format:
            <RA>,<DEC>,<MAG>

        RA:    0 ->  24
        DEC: +90 -> -90
        MAG: any floating-point value
        """
        matches = []
        for line in codecs.open(self.file_path, 'r', 'utf-8').readlines():
            parts = line.split(',')
            ra, dec, mag = list(map(float, parts[:3]))
            label = '' if len(parts) < 4 else parts[3]
            if mag > sky_area.mag_min: #because smaller mag values mean brighter stars
                continue
            if not (sky_area.ra_min <= ra <= sky_area.ra_max):
                continue
            if not (sky_area.dec_min <= dec <= sky_area.dec_max):
                continue

            matches.append(StarData(ra, dec, mag, label))

        return StarDataList(matches)
