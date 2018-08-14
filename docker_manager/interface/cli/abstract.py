import simpcli

from docker_manager.config import ManagerConfig
from docker_manager.docker.projects import Projects

from docker_manager.exceptions import NoProjectsFoundException


class BaseCommand(object):

    interface = simpcli.Interface()
    command = simpcli.Command(True)
    config = ManagerConfig()
    projects = None

    def __init__(self):
        self.config.load()
        try:
            self.projects = Projects()
        except NoProjectsFoundException:
            self.interface.writeOut('No projects found in your config')
