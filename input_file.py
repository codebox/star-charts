import codecs

class InputFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_stars(self, ra_range, dec_range, min_mag):
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
            ra, dec, mag = map(float, parts[:3])
            label = '' if len(parts) < 4 else parts[3]
            if mag > min_mag: #because smaller mag values mean brighter stars
                continue
            if not (ra_range[0] <= ra <= ra_range[1]):
                continue
            if not (dec_range[0] <= dec <= dec_range[1]):
                continue

            matches.append((ra, dec, mag, label))

        return matches
