# PYTHON_ARGCOMPLETE_OK

import sys
import argcomplete
import argparse

from docker_manager.interface.cli import Cli

if len(sys.argv) == 2:
    # default branch name is *
    sys.argv.append('all-projects')

if len(sys.argv) == 3:
    # default branch name is *
    sys.argv.append('all-services')

cli = Cli()

# create parser in order to autocomplete
parser = argparse.ArgumentParser()

parser.add_argument(
    "command",
    help="What command do you want to execute?",
    type=str,
    choices=cli.getAvailableCommands()
)

parser.add_argument(
    'project',
    help = 'On which project you want to execute the command on?',
    #choices = ['all-projects'],
    type = str
)

parser.add_argument(
    'services',
    help = 'On which service you want to execute the command on?',
    #choices = ['all-services'],
    type = str
)
argcomplete.autocomplete(parser)


def main():
    try:
        arguments = parser.parse_args()
        command = arguments.command
        project = arguments.project
        services = arguments.services
        cli.dispatch(command, project, services)
        sys.exit(0)
    except KeyboardInterrupt:
        cli.close("See you soon!")
        sys.exit(1)
