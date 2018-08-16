import os
import yaml

from docker_manager.exceptions import ConfigException
from docker_manager.exceptions import NoDockerComposeFileException
from docker_manager.exceptions import ProjectAlreadyAddedException
from docker_manager.exceptions import ProjectNotFoundException

from pprint import pprint


class Yaml:

    yaml = {}

    def load(self, filename: str):
        if not os.path.isfile(filename):
            raise ConfigException("Configfile %s not found" % filename)

        with open(filename, 'r') as stream:
            self.yaml = yaml.safe_load(stream)

        return self.yaml

    def write(self, filename: str, config: dict):
        filepath = os.path.dirname(filename)
        if not os.path.isdir(filepath):
            os.makedirs(filepath)

        with open(filename, "w") as outfile:
            outfile.write(yaml.dump(config, default_flow_style=False))


class BaseConfig:

    yaml = Yaml()
    config = None
    filename = None
    defaultConfig = {}

    def __init__(self):
        self.filename = os.path.expanduser(self.filename)

    def get(self):
        return self.config

    def load(self):
        try:
            self.config = self.yaml.load(self.filename)
        except ConfigException as e:
            self.config = self.defaultConfig
        return True

    def write(self):
        self.yaml.write(self.filename, self.config)
        return True



class ManagerConfig(BaseConfig):

    filename = '~/.docker-manager/config.yml'
    composerCongigs = []
    defaultConfig = {
        'projects': {}
    }

    def setProjects(self, projects):
        self.load()
        self.config['projects'] = projects

    def loadComposerConfigs(self):
        if 'projects' not in self.config or type(self.config['projects']) != dict:
            raise ConfigException('No projects specified in %' % (self.filename))
        for project in self.yaml['projects']:
            directory = os.path.expanduser(project)
            composerConfigfile = '%s/docker-compose.yml' % (directory)
            try:
                config = ComposerConfig(composerConfigfile)
                config.load()
                self.composerCongigs[composerConfigfile] = config
            except ConfigException:
                pass

class ComposeConfig(BaseConfig):
    filename = './docker-compose.yml'

    def debug(self):
        pprint(self.yaml)
