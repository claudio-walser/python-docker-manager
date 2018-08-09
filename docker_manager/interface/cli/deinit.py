import os

from docker_manager.interface.cli.abstract import BaseCommand
from docker_manager.exceptions import NoDockerComposeFileException
from docker_manager.exceptions import ProjectNotFoundException


class Deinit(BaseCommand):

    def run(self, project: str, services: str) -> bool:
        currentFolder = os.getcwd()
        try:
            self.config.removeProject(currentFolder)
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
