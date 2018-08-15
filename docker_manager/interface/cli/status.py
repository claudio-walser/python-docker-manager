from docker_manager.docker.compose import Compose
from docker_manager.docker.container import Container
from docker_manager.interface.cli.abstract import BaseCommand


class Status(BaseCommand):

    def run(self, project: str, services: str):
        if project == 'all-projects':
            for project in self.projects.getAll():
                self.status(project)
        else:
            self.status(project)
        return True

    def statusHeader(self):
        statusHeaderString = "ID".ljust(20)
        statusHeaderString += "NAME".ljust(40)
        statusHeaderString += "IP".ljust(15)
        statusHeaderString += "CREATED".ljust(10)
        statusHeaderString += "RUNNING".ljust(10)
        self.bold(statusHeaderString)

    def status(self, project):
        self.interface.writeOut('')
        self.bold(project)
        self.statusHeader()

        project = self.projects.getProject(project)
        project.changeWorkingDirectory()
        compose = Compose()
        for containerName in compose.getContainerNames():
            container = Container(containerName)
            statusString = str(container.getId()).ljust(20)
            statusString += str(container.name).ljust(40)
            statusString += str(container.getIpAddress()).ljust(15)
            statusString += str(container.isCreated()).ljust(10)
            statusString += str(container.isRunning()).ljust(10)
            self.interface.writeOut(statusString)
