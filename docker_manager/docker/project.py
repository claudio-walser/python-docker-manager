import os

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
        syncFile = '%s/docker-sync.yml' % (path)
        return os.isfile(syncFile)

    def changeWorkingDirectory(self):
        os.chdir(self.path)
