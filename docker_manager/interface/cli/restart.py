from docker_manager.docker.project import Project

from docker_manager.interface.cli.abstract import BaseCommand
from docker_manager.interface.cli.start import Start
from docker_manager.interface.cli.stop import Stop

class Restart(BaseCommand):

    def run(self, project: Project, services: str):
        self.interface.writeOut('Command status')
        startCommand = Start()
        stopCommand = Stop()

        stopCommand.stop(project, services)
        startCommand.start(project, services)

        return True
