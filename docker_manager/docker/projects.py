import os

from docker_manager.config import ManagerConfig
from docker_manager.docker.project import Project
#from docker_manager.exceptions import NoProjectsFoundException
from docker_manager.exceptions import ProjectNotFoundException
from docker_manager.exceptions import ProjectAlreadyAddedException
from docker_manager.exceptions import NoDockerComposeFileException


class Projects (object):

    projects = {}
    config = ManagerConfig()

    def __init__(self):
        self.config.load()

        config = self.config.get()
        if 'projects' not in config \
        or type(config['projects']) != dict \
        or len(config['projects']) == 0:
            projects = {}
        else:
            projects = config['projects']

        for projectPath in projects:
            try:
                project = Project(projects[projectPath])
                self.projects[project.getName()] = project
            except NoDockerComposeFileException:
                pass

    def getAll(self):
        return self.projects

    def getProject(self, project: str):
        self.checkProject(project)
        return self.projects[project]

    def add(self, path):
        composeFile = '%s/docker-compose.yml' % (path)
        if not os.path.isfile(composeFile):
            raise NoDockerComposeFileException("No docker-compose.yaml found in %s!" % path)

        projectName = os.path.basename(path)

        if projectName in self.projects:
            raise ProjectAlreadyAddedException('Project %s was already added earlier.' % (path))

        self.projects[projectName] = path
        
        self.config.setProjects(self.projects)
        return self.config.write()

    def remove(self, path):
        pass

    def checkProject(self, project):
        if project not in self.projects:
            raise ProjectNotFoundException('Project "%s" not found in your config!' % (project))
