

class ConfigException(Exception):
    pass

class NoDockerComposeFileException(Exception):
    pass

class NoProjectsFoundException(Exception):
    pass

class ProjectAlreadyAddedException(Exception):
    pass

class ProjectNotFoundException(Exception):
    pass

class DockerManagerException(Exception):
    pass
