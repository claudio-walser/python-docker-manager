from docker_manager.docker.sync import Sync
from docker_manager.docker.compose import Compose
from docker_manager.docker.project import Project

from docker_manager.interface.cli.abstract import BaseCommand

class Start(BaseCommand):

    def run(self, project: Project, services: str):
        project.changeWorkingDirectory()
        compose = Compose()
        compose.start()
        if project.hasDockerSync():
            sync = Sync()
            sync.start()
