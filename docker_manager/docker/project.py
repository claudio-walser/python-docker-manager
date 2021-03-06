import os

from docker_manager.exceptions import NoDockerComposeFileException


class Project (object):

    name = None
    path = None

    def __init__(self, path: str):
        composeFile = '%s/docker-compose.yml' % (path)
        if not os.path.isfile(composeFile):
            raise NoDockerComposeFileException("No docker-compose.yaml found in %s!" % path)

        self.path = path
        self.name = os.path.basename(path)

    def getName(self):
    	return self.name

    def getPath(self):
    	return self.path

    def hasDockerSync(self):
        syncFile = '%s/docker-sync.yml' % (self.path)
        return os.path.isfile(syncFile)

    def changeWorkingDirectory(self):
        os.chdir(self.path)
