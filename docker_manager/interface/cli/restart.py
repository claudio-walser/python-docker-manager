from docker_manager.interface.cli.abstract import BaseCommand


class Restart(BaseCommand):

    def run(self, project: str, services: str):
        self.interface.writeOut('Command restart')
        return True
