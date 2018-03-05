import csv
import random

from RealEstateAnalysis.Data.DataModel import DataSource

def new(file, encoding = None):
    return DataCsv(file, encoding)

class DataCsv(DataSource):

    @property
    def description(self):
        return "CSV Data from {0}".format(self.file)
    
    def __iter__(self):
        return super(DataCsv, self).__iter__()

    def __init__(self, file, encoding=None):
        DataSource.__init__(self)
        self.__file = file
        self.__encoding = encoding

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
        with open (self.file, "r", encoding=self.encoding) as csvfile:
            firstLine = csvfile.readline().split(',')
            headers = [ header.strip().lower().replace(" ", "_")
                        for header in firstLine
                      ]
            csvreader = csv.DictReader(csvfile, headers)
            self.data = [
                self.processor(row) for row in csvreader
                    if self.test(row)
            ]
            super().load()
        return self


            

    



    