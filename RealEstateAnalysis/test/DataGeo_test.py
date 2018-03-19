from unittest import TestCase, skip

from RealEstateAnalysis.Data import DataStream, DataCsv, DataGeo
from RealEstateAnalysis.Data.DataGeo import DataGeo as geo
from geojson import Polygon, MultiPolygon

class GeoCompTest(TestCase):
    def setUp(self):
        squareCoords = [ (0,0)
                       , (1,0)
                       , (1,1)
                       , (0,1)
                       , (0,0)
                       ]
        rectCoords = [ (1,2)
                     , (5,2)
                     , (5,5)
                     , (1,5)
                     , (1,2)
                     ]
        self.square = Polygon([
            squareCoords
        ])
        self.rectangle = Polygon([
            rectCoords
        ])
        self.multi = MultiPolygon([
            [ squareCoords ],
            [ rectCoords ]
        ])
    def tearDown(self):
        pass

    def test_area_square(self):
        self.assertEqual(geo.area(self.square), 1)

    def test_area_rectangle(self):
        self.assertEqual(geo.area(self.rectangle), 12)

    def test_centroid_square(self):
        a, b = geo.centroid(self.square)
        self.assertEqual(a, 1/2)
        self.assertEqual(b, 1/2)

    def test_centroid_rectangle(self):
        a, b = geo.centroid(self.rectangle)
        self.assertEqual(a, 3)
        self.assertEqual(b, 3.5)
    
    def test_area_multi(self):
        self.assertEqual(geo.area(self.multi), 13)

class GeoLoadTest(TestCase):
    def setUp(self):
        self.geoFrame = DataGeo.new("RealEstateAnalysis/SampleData/TaxParcels.json")
        self.geoFrame.load()
    def tearDown(self):
        pass
    
    def test_geo_frame_nonempty(self):
        self.assertGreater(len(self.geoFrame), 0)
    
    def test_geo_frame_can_compute_area(self):
        sample = self.geoFrame.sample(1)
        area = geo.area(sample[0]["geometry"])
        self.assertGreater(area, 0)

    def test_geo_frame_can_compute_centroid(self):
        sample = self.geoFrame.sample(1)[0]["geometry"]
        while sample["type"] != "Polygon":
            sample = self.geoFrame.sample(1)
        coords = list(zip(*sample["coordinates"][0]))
        minX = min(coords[0])
        minY = min(coords[1])
        maxX = max(coords[0])
        maxY = max(coords[1])
        centroid = geo.centroid(sample)
        self.assertGreater(centroid[0], minX)
        self.assertGreater(centroid[1], minY)
        self.assertLess(centroid[0], maxX)
        self.assertLess(centroid[1],maxY)
        
        