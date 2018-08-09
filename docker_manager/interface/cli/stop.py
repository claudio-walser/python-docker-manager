from docker_manager.interface.cli.abstract import BaseCommand


class Stop(BaseCommand):

    def run(self, project: str, services: str):
        self.interface.writeOut('Command stop')
        return True
