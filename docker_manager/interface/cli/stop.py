from docker_manager.docker.sync import Sync
from docker_manager.docker.compose import Compose
from docker_manager.docker.project import Project

from docker_manager.interface.cli.abstract import BaseCommand


class Stop(BaseCommand):

    def run(self, project: Project, services: str):
        project.changeWorkingDirectory()
        compose = Compose()
        compose.stop()
        if project.hasDockerSync():
            sync = Sync()
            sync.stop()
