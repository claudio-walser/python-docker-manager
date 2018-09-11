from docker_manager.docker.compose import Compose

from docker_manager.interface.cli.abstract import BaseCommand


class Update(BaseCommand):

    def run(self, project: str, services: str):
        self.interface.writeOut('Command update')
        if project == 'all-projects':
            for project in self.projects.getAll():
                self.update(project)
        else:
            self.update(project)
        return True

    def update(self, project):
        self.interface.writeOut('')
        self.bold(project)
        #self.interface.bold(project)
        project = self.projects.getProject(project)
        project.changeWorkingDirectory()
        compose = Compose()
        compose.pull()
        compose.start()
