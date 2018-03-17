import json
import os

from RealEstateAnalysis.Data.DataModel import DataSource

def new(file, dataPath=[], encoding=None):
    return DataJson(file, dataPath, encoding)

class DataJson(DataSource):

    @property
    def description(self):
        return "JSON data from {0}".format(self.file)
    
    def __iter__(self):
        return super().__iter__()
    
    def __init__(self, file, dataPath=[], encoding=None):
        DataSource.__init__(self)
        self.__file = file
        self.__encoding = encoding
        self.__dataPath = dataPath
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        self.__filePath = os.path.join(fileDir, file)

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
        with open (self.__filePath, "r", encoding=self.encoding) as jsonfile:
            data = json.load(jsonfile)
            if self.__dataPath is not None:
                for path in self.__dataPath:
                    data = data[path]
            self.data = [ self.selector(self.processor(row) )
                          for row in data
                          if self.test(row)
                        ]
        super().load()
        return self
