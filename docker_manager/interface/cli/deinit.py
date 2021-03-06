import os

from docker_manager.docker.project import Project

from docker_manager.interface.cli.abstract import BaseCommand
from docker_manager.exceptions import NoDockerComposeFileException
from docker_manager.exceptions import ProjectNotFoundException


class Deinit(BaseCommand):

    runPerProject = False

    def run(self, project: Project, services: str) -> bool:
        currentFolder = os.getcwd()
        try:
            self.projects.remove(currentFolder)
            self.interface.ok(
                'Path %s successfully removed to your projects.' % (
                    currentFolder
                )
            )
        except ProjectNotFoundException as e:
            self.interface.ok('This project was not found in your config.')
        except NoDockerComposeFileException as e:
            self.interface.error(e)
            return False

        return True
