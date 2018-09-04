import simpcli
import sys

from docker_manager.plugins.basicauth import BasicAuth
from docker_manager.plugins.nginx import Nginx
from docker_manager.plugins.hosts import Hosts

from docker_manager.config import ManagerConfig
from docker_manager.docker.projects import Projects
from docker_manager.docker.compose import Compose
from docker_manager.docker.container import Container


class BaseCommand(object):

    interface = simpcli.Interface()
    command = simpcli.Command(True)
    config = ManagerConfig()
    projects = None
    plugins = None

    def __init__(self):
        self.config.load()
        self.projects = Projects()
        className = self.__class__.__name__
        if self.projects.getAll() == {} and className != 'Init' and className != 'ExtraCommand':
            self.interface.error('No projects found in your config')
            self.interface.writeOut('To add a project navigate into a directory with a docker-compose.yml and execute docker-manager init.')
            self.exit()

    def exit(self):
        sys.exit(1)

    def bold(self, string):
        self.interface.writeOut('%s%s%s' % (self.interface.BOLD, string, self.interface.ENDC))

    def runPlugins(self, project):
        print('Plugin Context')
        try: 
            self.plugins = [
                # BasicAuth(),
                # Nginx(),
                Hosts()
            ]
            command = self.__class__.__name__.lower()
            project.changeWorkingDirectory()
            compose = Compose()
            for container in compose.getContainers():
                for plugin in self.plugins:
                    print('Call %s on plugin %s' % (command, type(plugin)))
                    plugin.run(command, container)
        except Exception as e:
            self.interface.error('Plugin Exception')
            self.interface.writeOut(e)
