from docker_manager.docker.sync import Sync
from docker_manager.docker.compose import Compose

from docker_manager.interface.cli.abstract import BaseCommand


class Stop(BaseCommand):

    def run(self, project: str, services: str):
        self.interface.writeOut('Command stop')
        if project == 'all-projects':
            for project in self.projects.getAll():
                self.stop(project)
        else:
            self.stop(project)
        return True

    def stop(self, project):
        self.interface.writeOut('')
        self.bold(project)
        #self.interface.bold(project)
        project = self.projects.getProject(project)
        project.changeWorkingDirectory()
        compose = Compose()
        compose.stop()
        if project.hasDockerSync():
            sync = Sync()
            sync.stop()