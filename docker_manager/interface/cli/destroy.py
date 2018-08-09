from docker_manager.interface.cli.abstract import BaseCommand


class Destroy(BaseCommand):

    def run(self, project: str, services: str):
        self.interface.writeOut('Command destroy')
        return True
