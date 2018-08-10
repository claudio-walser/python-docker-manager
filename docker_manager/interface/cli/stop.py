from docker_manager.docker.sync import Sync

from docker_manager.interface.cli.abstract import BaseCommand


class Stop(BaseCommand):

    def run(self, project: str, services: str):
        self.interface.writeOut('Command stop')
        if project == 'all-projects':
            for project in self.projects.getAll():
                self.stop(project)
        else:
            self.stop(project)
        return True

    def stop(self, project):
        self.interface.writeOut('%s%s:%s' % (self.interface.BOLD, project, self.interface.ENDC))
        #self.interface.bold(project)
        project = self.projects.getProject(project)
        project.changeWorkingDirectory()
        self.compose.stop()
        if project.hasDockerSync():
            sync = Sync()
            sync.stop()