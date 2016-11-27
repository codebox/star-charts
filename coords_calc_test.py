import unittest
from coord_calc import CoordCalc

class CoordCalcTest(unittest.TestCase):
    def setUp(self):
        pass

    def check_xy(self, cc, ra, dec, expected_x, expected_y):
        x,y = cc.convert_to_x_y(ra, dec)
        self.assertEqual(expected_x, x)
        self.assertEqual(expected_y, y)

    def test1(self):
        cc = CoordCalc(1, 2, 70, 80, 100)
        coords = [(1,70), (1,80), (2,70), (2,80)]
        r = cc.convert_to_x_y(coords)
        print r
        #self.check_xy(cc, 1, 70, 0, 0)
        #self.check_xy(cc, 2, 70, 100, 0)
        #self.check_xy(cc, 1, 80, 0, 100)
        #self.check_xy(cc, 2, 80, 100, 100)

if __name__ == '__main__':
    unittest.main()