from docker_manager.docker.sync import Sync
from docker_manager.docker.compose import Compose

from docker_manager.interface.cli.abstract import BaseCommand


class Destroy(BaseCommand):

    def run(self, project: str, services: str):
        self.interface.writeOut('Command destroy')
        if project == 'all-projects':
            for project in self.projects.getAll():
                self.destroy(project)
        else:
            self.destroy(project)
        return True

    def destroy(self, project):
        self.interface.writeOut('')
        self.bold(project)
        #self.interface.bold(project)
        project = self.projects.getProject(project)
        project.changeWorkingDirectory()
        compose = Compose()
        compose.destroy()
        if project.hasDockerSync():
            sync = Sync()
            sync.destroy()

        self.runPlugins(project)
