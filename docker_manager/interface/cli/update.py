from docker_manager.docker.compose import Compose
from docker_manager.docker.project import Project

from docker_manager.interface.cli.abstract import BaseCommand


class Update(BaseCommand):

    def run(self, project: Project, services: str):
        project.changeWorkingDirectory()
        compose = Compose()
        compose.pull()
        compose.start()
