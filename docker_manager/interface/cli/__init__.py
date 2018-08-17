import sys
import simpcli

from docker_manager.interface.cli.abstract import BaseCommand
from docker_manager.interface.cli.status import Status
from docker_manager.interface.cli.start import Start
from docker_manager.interface.cli.stop import Stop
from docker_manager.interface.cli.update import Update
from docker_manager.interface.cli.restart import Restart
from docker_manager.interface.cli.destroy import Destroy
from docker_manager.interface.cli.init import Init
from docker_manager.interface.cli.deinit import Deinit
from docker_manager.interface.cli.projects import Projects
from docker_manager.interface.cli.pull import Pull
from docker_manager.interface.cli.changedirectory import ChangeDirectory

from docker_manager.exceptions import DockerManagerException


class Cli():

    interface = simpcli.Interface()

    commands = [
        "status",
        "start",
        "stop",
        "update",
        "restart",
        "destroy",
        "init",
        "deinit",
        "projects",
        "pull",
        "cd"
    ]

    def getAvailableCommands(self):
        return self.commands

    def instantiateCommand(self, command: str) -> BaseCommand:
        if command == 'status':
            return Status()
        if command == 'start':
            return Start()
        if command == 'stop':
            return Stop()
        if command == 'update':
            return Update()
        if command == 'restart':
            return Restart()
        if command == 'destroy':
            return Destroy()
        if command == 'init':
            return Init()
        if command == 'deinit':
            return Deinit()
        if command == 'projects':
            return Projects()
        if command == 'pull':
            return Pull()
        if command == 'cd':
            return ChangeDirectory()

        raise DockerManagerException('Command "%s" not found!' % (command))

    def dispatch(self, command: str, project: str, service: str):
        try:
            commandObject = self.instantiateCommand(command)
        except Exception as e:
            raise e
            errorMessage = 'Command %s failed,' + \
                ' Exception was: %s'

            self.interface.error(
                errorMessage % (
                    command,
                    e
                )
            )
            sys.exit(1)

        self.interface.header('docker-manager %s' % (command))

        try:
            commandObject.run(project, service)
        # catch cli execution errors here
        except (DockerManagerException, simpcli.CliException) as e:
            self.interface.error(format(e))

    def close(self, msg: str):
        self.interface.ok(msg)