import abc
import random
import pandas
from collections import defaultdict
from RealEstateAnalysis.Notifications.Deprecation import deprecated

class DataSource(abc.ABC):

    def __init__(self):
        self.__data = []
        self.__len = 0
        self.__postProcess = None
        self.__select = None
        self.__params = None
        self.__loaded = False
        self.__test = None
    #data
    @property
    def data(self):
        return self.__data
        
    @data.setter
    def data(self, x):
        self.__data = x
    
    def selectKey(self, key):
        return lambda x: x[key]

    def select(self, keys=[], **kwargs):
        if self.__select == None:
            self.__select = {}
        for arg in keys:
            self.__select[arg] = self.selectKey(arg)
        for arg in kwargs:
            self.__select[arg] = kwargs[arg]
        return self

    @abc.abstractmethod
    def __iter__(self):
        return iter(self.__data)

    def __getitem__(self, n):
        return self.__data[n]

    @property
    def loaded(self):
        return self.__loaded

    @loaded.setter
    def loaded(self, boolean):
        self.__loaded = boolean

    @abc.abstractmethod
    def load(self):
        self.__loaded = True
        self.length = len(self.data)
        return self
    # length
    @property
    def length(self):
        return self.__len

    @length.setter
    def length(self, n):
         self.__len = n

    def __len__(self):
        return self.__len

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, param):
        self.__params = param

    # Description
    @property    
    @abc.abstractmethod
    def description(self):
        return None

    def sample(self, n):
        L = self.__data
        if n < len(self):
            self.__len = self.__len - n
            output =[
                L.pop(random.randrange(len(L)))
                for _ in range(n)
            ]
            return new(output)
        else:
            output = [item for item in self]
            self.__data = []
            self.__len = 0
            return new(output)

    def where (self, test = None, **kwargs):
        if self.__params is None and len(kwargs)>0 :
            self.__params = {}
        if callable(test):
            if self.__test is None:
                self.__test = []
            self.__test.append(test)
        for key in kwargs:
            self.__params[key] = kwargs[key]
        return self

    def test(self, input):        
        if self.__test is not None:
            for test in self.__test:
                if not test(input):
                    return False
        return self.__testParams(input)
    
    def __testParams(self, input):
        if self.__params is not None:
            for key in set(self.__params).intersection(input):
                if (self.__params[key] != input[key]):
                    return False
        return True

    @deprecated("processor", "1.1")
    def processor(self, input):
        if self.__postProcess is None:
            return input
        else:
            for key in set(self.__postProcess).intersection(input):
                input[key] = self.__postProcess[key](input[key])
            return input
    
    def selector(self, input):
        if self.__select is None:
            return input
        else:
            output = {}
            for key in self.__select:
                output[key] = self.__select[key](input)
            return output

    @deprecated("process", "1.1")
    def process(self, **kwargs):
        if self.__postProcess is None:
            self.__postProcess = defaultdict(lambda x: x)
        for key in kwargs:
            fun = kwargs[key]
            if callable(fun):
                self.__postProcess[key] = fun
        return self

    def reset(self):
        self.__postProcess = None
        self.__params = None
        self.__test = None
        self.__len = len(self.__data)
        self.__loaded = False
        return self

    def export(self, exportArray):
        output = [ [x[export] for export in exportArray] for x in self.__data ]
        return DataArray(output)

    def dataFrame(self):
        return pandas.DataFrame(self.data)

def new(dataArray):
    return DataArray(dataArray)

class DataArray(DataSource):

    def __init__(self, dataArray):
        super().__init__()
        self.__original = dataArray
        self.loaded = True
        #Duck Typing
        self.length = len(dataArray)
        array = [x for x in dataArray]
        self.data = array
    
    def __iter__(self):
        return DataSource.__iter__(self)

    def load(self):
        self.__data = [ self.selector(self.processor(x)) 
                        for x in self.__original 
                        if self.test(x)
                      ]
        self.__len = len(self.__data)
        super().load()
        return self

    @property
    def description(self):
        if self.length == 0:
            return "Empty Array"
        else:
            return "Array of items {0}".format(self.data[0])

    def reset(self):
        DataSource.reset(self)
        self.data = self.__original
        self.loaded = True
        return self
    

