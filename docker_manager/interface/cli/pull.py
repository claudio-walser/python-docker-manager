from docker_manager.docker.compose import Compose

from docker_manager.interface.cli.abstract import BaseCommand

class Pull(BaseCommand):

    def run(self, project: str, services: str):
        self.interface.writeOut('Command pull')
        if project == 'all-projects':
            for project in self.projects.getAll():
                self.pull(project)
        else:
            self.pull(project)
        return True

    def pull(self, project):
        self.interface.writeOut('')
        self.bold(project)
        project = self.projects.getProject(project)
        project.changeWorkingDirectory()
        compose = Compose()
        compose.pull()

        self.runPlugins(project)
