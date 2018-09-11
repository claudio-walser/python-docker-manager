from docker_manager.docker.compose import Compose
from docker_manager.docker.project import Project

from docker_manager.interface.cli.abstract import BaseCommand


class Status(BaseCommand):

    def run(self, project: Project, services: str):
        self.statusHeader()

        project.changeWorkingDirectory()
        compose = Compose()
        for container in compose.getContainers():
            statusString = str(container.getId()).ljust(20)
            statusString += str(container.name).ljust(40)
            statusString += str(container.getIpAddress()).ljust(15)
            statusString += str(container.isCreated()).ljust(10)
            statusString += str(container.isRunning()).ljust(10)
            self.interface.writeOut(statusString)

    def statusHeader(self):
        statusHeaderString = "ID".ljust(20)
        statusHeaderString += "NAME".ljust(40)
        statusHeaderString += "IP".ljust(15)
        statusHeaderString += "CREATED".ljust(10)
        statusHeaderString += "RUNNING".ljust(10)
        self.bold(statusHeaderString)
