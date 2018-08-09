from docker_manager.interface.cli.abstract import BaseCommand


class Projects(BaseCommand):

    def run(self, project: str, services: str) -> bool:
        projects = self.projects.getAll()

        for project in projects:
        	self.interface.writeOut('')
        	self.interface.writeOut('%s%s:%s' % (self.interface.BOLD, project, self.interface.ENDC))
        	self.interface.writeOut(projects[project].getPath())

        return True
