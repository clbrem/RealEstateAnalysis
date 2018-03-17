import requests
import random
from RealEstateAnalysis.Data.DataModel import DataSource, DataArray

def new (url):
    return DataStream(url)

class DataStream(DataSource):
    @property
    def description(self):
        return "Data Stream from {0}".format(self.url)
    
    def __iter__(self):
        return super().__iter__()

    def __init__(self, url, key=None):
        super.__init__()
        self.__url = url
        self.__key = key

    @property 
    def url(self):
        return self.__url

    def load(self):
        a = requests.get(self.url, self.params)
        self.data = a.json()
        super().load()
        return self
