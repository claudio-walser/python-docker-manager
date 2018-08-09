from docker_manager.interface.cli.abstract import BaseCommand


class Update(BaseCommand):

    def run(self, project: str, services: str):
        self.interface.writeOut('Command update')
        return True
