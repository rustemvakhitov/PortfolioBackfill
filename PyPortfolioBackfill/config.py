import json


class Config():

    def __init__(self):
        configfile = open('config.json',)
        self.Config = json.load(configfile) 
        self.ProjectsRoot = self.getConfigKey('projects-root', default=None)
        self.TagsRoot = self.getConfigKey('tags-root', default=None)
        self.TagsFile = self.getConfigKey('tags-file', default=None)
        self.BucketName = self.getConfigKey('bucket-name', default=None)
        self.Region = self.getConfigKey('region', default=None)
        self.ProjectsTableName = self.getConfigKey('projects-table-name', default=None)
        self.TagsTableName = self.getConfigKey('tags-table-name', default=None)

        return

    def getConfigKey(self, key, default=None):
        settings = self.Config['settings']
        value = settings[key]
        
        return value

    def __str__(self):
        return f'Instance of Config class ProjectsRoot == {self.ProjectsRoot} TagsRoot == {self.TagsRoot} TagsFile == {self.TagsFile}'
    
    def __repr__(self):
        return f'Instance of Config class ProjectsRoot == {self.ProjectsRoot} TagsRoot == {self.TagsRoot} TagsFile == {self.TagsFile}'