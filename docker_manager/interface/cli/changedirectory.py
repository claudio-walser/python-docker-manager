from docker_manager.interface.cli.abstract import BaseCommand
import subprocess
import os
from pprint import pprint


class ChangeDirectory(BaseCommand):

    def run(self, project: str, services: str) -> bool:
        config = self.config.get()
        if 'projects' not in config \
        or type(config['projects']) != dict \
        or len(config['projects']) == 0:
        	self.interface.writeOut('No projects found in your config')
        if project not in config['projects']:
            self.interface.error('Project %s not found in your config!' % (project))

        os.chdir(config['projects'][project])
        #self.command.execute('pwd')
        handle = subprocess.Popen('/bin/bash')
        handle.communicate('bash -l && cd %s' % (config['projects'][project]))

        return True
