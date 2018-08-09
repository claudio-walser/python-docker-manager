from docker_manager.docker.sync import Sync

from docker_manager.interface.cli.abstract import BaseCommand

class Start(BaseCommand):

    def run(self, project: str, services: str):
        self.interface.writeOut('Command status')
        if project == 'all-projects':
            for project in self.projects.getAll():
                self.start(project)
        else:
            self.start(project)
        return True

    def start(self, project):
        self.interface.writeOut('%s%s:%s' % (self.interface.BOLD, project, self.interface.ENDC))            
        #self.interface.bold(project)            
        project = self.projects.getProject(project)
        project.changeWorkingDirectory()
        self.compose.start()
        if project.hasDockerSync():
            sync = Sync()
            sync.start()