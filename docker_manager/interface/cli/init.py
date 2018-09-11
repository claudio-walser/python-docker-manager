import os

from docker_manager.docker.project import Project

from docker_manager.interface.cli.abstract import BaseCommand

from docker_manager.exceptions import NoDockerComposeFileException
from docker_manager.exceptions import ProjectAlreadyAddedException


class Init(BaseCommand):

    runPerProject = False

    def run(self, project: Project, services: str) -> bool:
        currentFolder = os.getcwd()
        try:
            self.projects.add(currentFolder)
            self.interface.ok(
                'Path %s successfully added to your projects.' % (
                    currentFolder
                )
            )
        except ProjectAlreadyAddedException:
            self.interface.ok('This project is already in your config.')
            return False
        except NoDockerComposeFileException as e:
            self.interface.error(e)
            return False

        return True
