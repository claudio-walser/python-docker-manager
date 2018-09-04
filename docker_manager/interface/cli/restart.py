from docker_manager.interface.cli.abstract import BaseCommand
from docker_manager.interface.cli.start import Start
from docker_manager.interface.cli.stop import Stop

class Restart(BaseCommand):

    def run(self, project: str, services: str):
        self.interface.writeOut('Command status')
        startCommand = Start()
        stopCommand = Stop()
        if project == 'all-projects':
            for project in self.projects.getAll():
                stopCommand.stop(project)
                startCommand.start(project)
        else:
            stopCommand.stop(project)
            startCommand.start(project)

        return True
