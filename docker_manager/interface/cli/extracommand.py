import subprocess
import os
import glob

from docker_manager.interface.cli.abstract import BaseCommand

from docker_manager.exceptions import NoExtraCommandFoundException

from pprint import pprint


class ExtraCommand(BaseCommand):

    commandStr = None
    extraCommandsDirectory = 'docker-manager'

    def __init__(self, command: str):
        self.commandStr = command
        super(ExtraCommand, self).__init__()

    def run(self, project: str, services: str) -> bool:
        project = self.projects.getProject(project)
        project.changeWorkingDirectory()
        print(self.commandStr)
        print('%s/%s/%s*' % (os.getcwd(), self.extraCommandsDirectory, self.commandStr))
        files = glob.glob('%s/%s/%s*' % (os.getcwd(), self.extraCommandsDirectory, self.commandStr))
        pprint(files)
        if len(files) == 0:
            raise NoExtraCommandFoundException('No extra command found for %s' % (self.commandStr))
        for file in files:
            self.command.execute(file)

        return True
