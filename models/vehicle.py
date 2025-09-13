from client.resource import ApiResource
from models.errors import ErrorParameterNotValid
class Vehicle(ApiResource):
    def __init__(self, name:str, model:str):
        self._name = name
        self._model = model

    @property
    def name(self):
        return self._name
    @property
    def model(self):
        return self._model

    @name.setter
    def name(self, new_name:str):
        if not isinstance(new_name,str):
            raise ErrorParameterNotValid(f"The paramater 'new_name'"
                                                 f"must be string")
        self._name = new_name

    @classmethod
    def from_api_response(cls, data:dict):
        vehicle = Vehicle(data["name"],data["model"])
        return vehicle

    def __str__(self):
        return (f"Name : {self.name} - Model : {self.model}")
