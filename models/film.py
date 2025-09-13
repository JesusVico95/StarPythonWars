from __future__ import annotations
from typing import List
from client.resource import ApiResource

class Film(ApiResource):
    def __init__(self, title:str=None, episode:int=None):
       self._title = title
       self._episode = episode

    @classmethod
    def from_api_response(cls,films:dict):
        film = Film(films["title"],films["episode_id"])
        return film

    def __str__(self):
        return f"Episode: {self._episode} {self._title}"
