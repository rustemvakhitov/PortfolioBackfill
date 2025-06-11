import json
from dataclasses import dataclass

@dataclass
class Project():
    id: int
    key: str
    name: str
    synopsis: str
    description: str
    projectRepositoryLink: str
    pictures: list[str]
    tags: list[str] 

    def toJSON(self):
           return json.dumps(self.__dict__)  

    @classmethod
    def fromJSON(cls, file_path):
        data = json.load(open(file_path))
        return cls(**data) 

    def __str__(self):
        return f'Instance of Project == {self.toJSON()}'
    
    def __repr__(self):
        return f'Instance of Project == {self.toJSON()}'