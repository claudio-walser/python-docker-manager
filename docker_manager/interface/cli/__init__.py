import sys
import simpcli

from docker_manager.docker.projects import Projects
from docker_manager.docker.project import Project
from docker_manager.docker.compose import Compose

from docker_manager.plugins.basicauth import BasicAuth
from docker_manager.plugins.nginx import Nginx
from docker_manager.plugins.hosts import Hosts

from docker_manager.interface.cli.abstract import BaseCommand
from docker_manager.interface.cli.status import Status as StatusCommand
from docker_manager.interface.cli.start import Start as StartCommand
from docker_manager.interface.cli.stop import Stop as StopCommand
from docker_manager.interface.cli.update import Update as UpdateCommand
from docker_manager.interface.cli.restart import Restart as RestartCommand
from docker_manager.interface.cli.destroy import Destroy as DestroyCommand
from docker_manager.interface.cli.init import Init as InitCommand
from docker_manager.interface.cli.deinit import Deinit as DeinitCommand
from docker_manager.interface.cli.projects import Projects as ProjectsCommand
from docker_manager.interface.cli.pull import Pull as PullCommand
from docker_manager.interface.cli.changedirectory import ChangeDirectory as ChangeDirectoryCommand
from docker_manager.interface.cli.extracommand import ExtraCommand

from docker_manager.exceptions import DockerManagerException
from docker_manager.exceptions import CommandNotFoundException
from docker_manager.exceptions import NoExtraCommandFoundException

from pprint import pprint


class Cli():

    interface = simpcli.Interface()
    command = simpcli.Command(True)
    projects = Projects()
    plugins = []
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

    commandsNotRunningByProjects = [
        'init',
        'deinit',
        'projects'
    ]

    def getAvailableCommands(self):
        return self.commands


    def instantiateCommand(self, command: str) -> BaseCommand:
        if command == 'status':
            return StatusCommand()
        if command == 'start':
            return StartCommand()
        if command == 'stop':
            return StopCommand()
        if command == 'update':
            return UpdateCommand()
        if command == 'restart':
            return RestartCommand()
        if command == 'destroy':
            return DestroyCommand()
        if command == 'init':
            return InitCommand()
        if command == 'deinit':
            return DeinitCommand()
        if command == 'projects':
            return ProjectsCommand()
        if command == 'pull':
            return PullCommand()
        if command == 'cd':
            return ChangeDirectoryCommand()

        raise CommandNotFoundException('Command "%s" not found!' % (command))

    def bold(self, string):
        self.interface.writeOut('%s%s%s' % (self.interface.BOLD, string, self.interface.ENDC))

    def dispatch(self, command: str, project: str, service: str):
        projects = []

        if project == 'all-projects':
            for project in self.projects.getAll():
                projects.append(project)
        else:
            projects.append(project)

        self.interface.header('docker-manager %s' % (command))
        extraCommandObject = ExtraCommand(command)


        if command in self.commandsNotRunningByProjects:
            self.runCommand(command, project, service)
        else:
            for project in projects:
                self.interface.writeOut('')
                self.bold(project)
                self.runCommand(command, project, service)



    def runCommand(self, command: str, project: str, service: str):
        project = self.projects.getProject(project)
        extraCommandObject = ExtraCommand(command)
        try:
            commandObject = self.instantiateCommand(command)
        except CommandNotFoundException:
            # if default command fails, try to find some extra commands
            try:
                extraCommandObject.run(project, service)
            except NoExtraCommandFoundException:
                # if not even an extraCommand is found, output an error
                errorMessage = 'Neither a command nor an extraCommand with the name "%s" was found in project "%s".'

                self.interface.error(
                    errorMessage % (
                        command,
                        project
                    )
                )
                pass

        try:
            commandObject.run(project, service)
            self.runPlugins(command, project)
            try:
                # try running additional commands stored in projects
                extraCommandObject.run(project, service)
            except NoExtraCommandFoundException:
                pass

        # catch cli execution errors here
        except UnboundLocalError:
            pass
        except Exception as e:
            errorMessage = 'An error occured\n' + \
                ' Exception was: %s'

            self.interface.error(
                errorMessage % (
                    e
                )
            )

            self.interface.error(format(e))

    def runPlugins(self, command, project):
        self.interface.info('Running plugins')
        try:
            self.plugins = [
                # BasicAuth(),
                # Nginx(),
                Hosts()
            ]
            project.changeWorkingDirectory()
            compose = Compose()
            for plugin in self.plugins:
                self.interface.writeOut('')
                self.bold(plugin.name)
                for container in compose.getContainers():
                    self.interface.writeOut(plugin.description % (container.getName()))
                    plugin.run(command, container)
        except Exception as e:
            self.interface.error('Plugin Exception')
            self.interface.writeOut(e)

    def close(self, msg: str):
        self.interface.ok(msg)