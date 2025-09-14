from __future__ import annotations
from client.resource import ApiResource

class Film(ApiResource):
    def __init__(self, title:str=None, episode:int=None):
       self._title = title
       self._episode = episode

    @classmethod
    def from_api_response(cls, films:dict):
        return cls(title=films["title"],episode=films["episode_id"])

    def __str__(self):
        return f"Episode: {self._episode} {self._title}"
