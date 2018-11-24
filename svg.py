XML_HEADER = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
SVG_HEADER = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">'
SVG_FOOTER = '</svg>'

class Svg:
    def __init__(self):
        self.elements = []

    def line(self, x1, y1, x2, y2, width, colour):
        self.elements.append('<line x1="{}" y1="{}" x2="{}" y2="{}" stroke-width="{}" stroke="{}"/>'.format(x1, y1, x2, y2, width, colour))

    def text(self, x, y, l, colour, size, align='left', decoration='None'):
        self.elements.append('<text x="{}" y="{}" text-anchor="{}" text-decoration="{}" style="fill: {}; font-size: {}px; font-family: monospace">{}</text>'.format(x, y, align, decoration, colour, size, l))

    def circle(self, x, y, d, colour):
        self.elements.append('<circle cx="{}" cy="{}" r="{}" fill="{}" />'.format(x, y, d, colour))

    def curve(self, _points, width, colour):
        points = sum(_points, ())

        # http://schepers.cc/getting-to-the-point
        d = 'M {} {} '.format(points[0], points[1])
        i = 0
        iLen = len(points)
        while iLen - 2 > i:
            p = []
            if i == 0:
                p.append((points[i],     points[i + 1]))
                p.append((points[i],     points[i + 1]))
                p.append((points[i + 2], points[i + 3]))
                p.append((points[i + 4], points[i + 5]))
            elif iLen - 4 == i:
                p.append((points[i - 2], points[i - 1]))
                p.append((points[i],     points[i + 1]))
                p.append((points[i + 2], points[i + 3]))
                p.append((points[i + 2], points[i + 3]))
            else:
                p.append((points[i - 2], points[i - 1]))
                p.append((points[i],     points[i + 1]))
                p.append((points[i + 2], points[i + 3]))
                p.append((points[i + 4], points[i + 5]))

            i += 2

            bp = []
            bp.append((p[1][0], p[1][1]))
            bp.append((((-(p[0][0]) + 6*p[1][0] + p[2][0]) / 6), (-(p[0][1]) + 6*p[1][1] + p[2][1]) / 6))
            bp.append((((  p[1][0]  + 6*p[2][0] - p[3][0]) / 6), (  p[1][1]  + 6*p[2][1] - p[3][1]) / 6))
            bp.append((p[2][0], p[2][1]))

            d += 'C {} {},{} {},{} {} '.format(bp[1][0], bp[1][1], bp[2][0], bp[2][1], bp[3][0], bp[3][1])

        self.elements.append('<path d="{}" stroke="{}" stroke-width="{}" fill="transparent"/>'.format(d, colour, width))

    def to_list(self):
        return [XML_HEADER, SVG_HEADER] + self.elements + [SVG_FOOTER]