# print(f"Signal_module : {__name__}")
from abc import ABC, abstractmethod

## kwarg is dict() have keys is indicator names and value is a tupple(params, value)
class signal(ABC): 
    indicators: list
    name : str
         
    @abstractmethod    
    def signal(self):
        pass
    def getIndicator(self):
        return self.indicators
    def getName(self):
        return self.name