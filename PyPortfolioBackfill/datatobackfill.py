import json
import config
import os
import project


class DataToBackfill():

    def __init__(self, config):
        self.Config = config

    def getTags(self):
        pathToTags = os.path.join(self.Config.TagsRoot, self.Config.TagsFile)
        configfile = open(pathToTags,)

        tags = json.load(configfile)

        return tags

    def getProjects(self):
        projects = list()

        for subfolder in os.scandir(self.Config.ProjectsRoot):
            if subfolder.is_dir():
                project = self.getProject(subfolder.path)

                if project is not None:
                    projects.append(project)

        return projects
    
    def getProject(self, pathToProject):
        pathToProjectFile = os.path.join(pathToProject, 'project.json')

        if not os.path.exists(pathToProjectFile):
            return None

        projectfile = open(pathToProjectFile,)
        proj: project.Project = project.Project.fromJSON(pathToProjectFile)
        proj.pictures = self.getProjectPictures(pathToProject)

        return proj
    
    def getProjectPictures(self, pathToProject):
        pathToProjectPictures = os.path.join(pathToProject, 'pictures')

        if not os.path.exists(pathToProjectPictures):
            return None

        pictures = list()

        for picture in os.scandir(pathToProjectPictures):
            if picture.is_file():
                pictures.append(picture.path)
       
        return pictures
    
    def __str__(self):
        return f'Instance of Config class ProjectsRoot == {self.ProjectsRoot} '
    
    def __repr__(self):
        return f'Instance of Config class ProjectsRoot == {self.ProjectsRoot}'