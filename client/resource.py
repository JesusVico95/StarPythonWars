from abc import ABC, abstractmethod
class ApiResource(ABC):
    @classmethod
    @abstractmethod
    def from_api_response(cls, data:dict):
        pass
