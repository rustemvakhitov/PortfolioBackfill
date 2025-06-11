import json


class Project():

    def __init__(self):
        self.id = None
        self.key = None
        self.name = None
        self.synopsis = None
        self.description = None
        self.projectRepositoryLink = None
        self.pictures = ["Ford", "Volvo", "BMW"]
        self.tags = ["Ford", "Volvo", "BMW"]

    def toJSON(self):
           return json.dumps(self.__dict__)    

    def __str__(self):
        return f'Instance of Project == {self.toJSON()}'
    
    def __repr__(self):
        return f'Instance of Project == {self.toJSON()}'