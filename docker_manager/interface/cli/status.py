from docker_manager.docker.compose import Compose

from docker_manager.interface.cli.abstract import BaseCommand


class Status(BaseCommand):

    def run(self, project: str, services: str):
        self.interface.writeOut('Command status')
        if project == 'all-projects':
            for project in self.projects.getAll():
                self.status(project)
        else:
            self.status(project)
        return True

    def status(self, project):
        self.interface.writeOut('%s%s:%s' % (self.interface.BOLD, project, self.interface.ENDC))
        #self.interface.bold(project)
        project = self.projects.getProject(project)
        project.changeWorkingDirectory()
        compose = Compose()
        compose.status()