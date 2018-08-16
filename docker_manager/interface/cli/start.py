from docker_manager.docker.sync import Sync
from docker_manager.docker.compose import Compose

from docker_manager.interface.cli.abstract import BaseCommand

class Start(BaseCommand):

    def run(self, project: str, services: str):
        self.interface.writeOut('Command start')
        if project == 'all-projects':
            for project in self.projects.getAll():
                self.start(project)
        else:
            self.start(project)
        return True

    def start(self, project):
        self.interface.writeOut('')
        self.bold(project)
        #self.interface.bold(project)
        project = self.projects.getProject(project)
        project.changeWorkingDirectory()
        compose = Compose()
        compose.start()
        if project.hasDockerSync():
            sync = Sync()
            sync.start()