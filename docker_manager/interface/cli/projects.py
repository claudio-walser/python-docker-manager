from docker_manager.docker.project import Project

from docker_manager.interface.cli.abstract import BaseCommand


class Projects(BaseCommand):

    runPerProject = False

    def run(self, project: Project, services: str) -> bool:
        projects = self.projects.getAll()

        for project in projects:
            self.interface.writeOut('')
            self.bold(project)
            self.interface.writeOut(projects[project].getPath())

        return True
