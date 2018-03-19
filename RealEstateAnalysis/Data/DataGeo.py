import geojson
import os
from RealEstateAnalysis.Notifications.Deprecation import deprecated
from RealEstateAnalysis.Data.DataModel import DataSource

def new(file, encoding = None):
    return DataGeo(file, encoding)

class DataGeo(DataSource):

    @property
    def description(self):
        return "GeoJson data from {0}".format(self.file)

    def __iter__(self):
        super().__iter__()

    def __init__(self, file, encoding=None):
        DataSource.__init__(self)
        self.__file = file
        self.__encoding = encoding
        fileDir = os.path.dirname(os.path.realpath('__file__'))        
        self.__filePath = os.path.join(fileDir, file)
        self.__geoType = None

    @property
    def geoType(self):
        return self.__geoType

    @property
    def encoding(self):
        return self.__encoding
    
    @property
    def file(self):
        return self.__file

    def reset(self):
        self.data = []
        super().reset()
        return self

    def load(self):
        with open(self.__filePath, "r", encoding=self.encoding) as geojsonfile:
            data = geojson.load(geojsonfile)
            geotype = data["type"]            
            if geotype == "FeatureCollection":
                self.__geoType = geotype
                dataArray = data["features"]
            elif geotype == "GeometryCollection":
                dataArray = data["geometries"]
                self.__geoType = geotype
            else:
                dataArray = []
            self.data = [ self.selector(datum) 
                          for datum in dataArray
                          if self.test(datum)
                        ]
            super().load()

    @deprecated("process", "1.1")
    def process(self, **kwargs):
        raise NotImplementedError

    @staticmethod
    def signedArea(geo):
        def polyArea(array):
            def simpleArea(array):
                a = 0
                for i in range(len(array)-1):
                    l = array [i]
                    r = array[i+1]
                    a += (l[0]*r[1] -l[1]*r[0])
                return a / 2
            return sum(simpleArea(item) for item in array)
        def areaRec(geo):
            geoType = geo["type"]
            if geoType in [ "Point"
                           , "MultiPoint"
                           , "LineString"
                           , "MultiLineString" ]:
                return 0
            elif geoType == "Polygon":
                return polyArea(geo["coordinates"])
            elif geoType == "MultiPolygon":
                return sum([polyArea(item) for item in geo["coordinates"] ])
            elif geoType == "GeometryCollection":
                return sum([areaRec(item) for item in geoType["geometries"]])
            elif geoType == "Feature":
                return areaRec(geo["geometry"])
            elif geoType == "FeatureCollection":
                return sum([areaRec(item) for item in geoType["features"]])

        return areaRec(geo)

    @staticmethod
    def area(geo):
        return abs(DataGeo.signedArea(geo))

    @staticmethod
    def centroid(geo):
        area = DataGeo.signedArea(geo)
        if area == 0:
            raise ZeroDivisionError
        def scaledPoly(array):
            def scaledSimple(array):
                a, b = 0, 0
                for i in range(len(array)-1):
                    l = array [i]
                    r = array[i+1]
                    a += (l[0] + r[0]) * (l[0]*r[1] -l[1]*r[0])
                    b += (l[1] + r[1]) * (l[0]*r[1] -l[1]*r[0])
                return (a,b)
            return sum(scaledSimple(poly)[0] for poly in array), \
                   sum(scaledSimple(poly)[1] for poly in array)
        def scaledRec(geo):
            geoType = geo["type"]
            if geoType in [ "Point"
                           , "MultiPoint"
                           , "LineString"
                           , "MultiLineString" ]:
                return 0
            elif geoType == "Polygon":
                return scaledPoly(geo["coordinates"]) 
                
            elif geoType == "MultiPolygon":
                a = sum([scaledPoly(item)[0] for item in geo["coordinates"] ])
                b = sum([scaledPoly(item)[1] for item in geo["coordinates"] ])
                return a, b
            elif geoType == "GeometryCollection":
                a = sum([scaledRec(item)[0] for item in geoType["geometries"]])
                b = sum([scaledRec(item)[1] for item in geoType["geometries"]])
                return a, b
            elif geoType == "Feature":
                a, b = scaledRec(geo["geometry"])
                return a,b
            elif geoType == "FeatureCollection":
                a = sum([scaledRec(item)[0] for item in geoType["features"]])
                b = sum([scaledRec(item)[1] for item in geoType["features"]])
                return a, b
        a, b = scaledRec(geo)
        return a / (6*area), b / (6*area)

    def selectKey(self, key):
        return lambda x: x["properties"][key]
