import simpcli
import sys


from docker_manager.config import ManagerConfig
from docker_manager.docker.projects import Projects


class BaseCommand(object):

    interface = simpcli.Interface()
    command = simpcli.Command(True)
    config = ManagerConfig()
    projects = None

    def exit(self):
        sys.exit(1)

    def bold(self, string):
        self.interface.writeOut('%s%s%s' % (self.interface.BOLD, string, self.interface.ENDC))

    def __init__(self):
        self.config.load()
        self.projects = Projects()
        if self.projects.getAll() == {} and self.__class__.__name__ != 'Init':
            self.interface.error('No projects found in your config')
            self.interface.writeOut('To add a project navigate into a directory with a docker-compose.yml and execute docker-manager init.')
            self.exit()
