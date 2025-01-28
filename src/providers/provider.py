from abc import ABC, abstractmethod
from pathlib import Path
class Provider(ABC):
    
    def __init__(self):
        pass

    @abstractmethod
    def get_bills():
        pass

    @abstractmethod
    def create_bill():
        pass
    
    @abstractmethod
    def get_time_entries():
        pass

