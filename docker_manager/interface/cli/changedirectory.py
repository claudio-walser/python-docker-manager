import subprocess
import os

from docker_manager.docker.project import Project

from docker_manager.interface.cli.abstract import BaseCommand


class ChangeDirectory(BaseCommand):

    def run(self, project: Project, services: str) -> bool:
       pass