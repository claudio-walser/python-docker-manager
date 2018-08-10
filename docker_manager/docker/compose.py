import os

from simpcli import Command as CliCommand

from docker_manager.config import ComposeConfig


class Compose (object):

  command = CliCommand(True)
  binary = 'docker-compose'
  dockerBinary = 'docker'

  def __init__(self):
    composeFile = './docker-compose.yml'
    if not os.path.isfile(composeFile):
        raise NoDockerComposeFileException("No docker-compose.yaml found in %s!" % path)
    composeConfig = ComposeConfig()
    composeConfig.load(composeFile)
    composeConfig.debug()

  def comopose(self, command, service = ''):
    if service == 'all-services':
      service = ''
    return self.command.execute('%s %s %s' % (self.binary, command, service))

  def start(self):
    return self.comopose('up -d')

  def stop(self):
    return self.comopose('stop')

  def status(self):
    return self.comopose('top')

  def destroy(self):
    self.stop()
    return self.comopose('rm -f')

  def update(self):
    return self.comopose('update')

  def restart(self):
    output = ''
    output += self.stop()
    output += self.start()
    return output

  def getContainerNames(self):
    # docker-compose ps -q $service
    # docker inspect --format='{{.Name}}' d487a433132b921eca0d94dc04dbca6af0a7bfbc8d29c511b256ffa795fa88c9
    raise Exception('Not implemented yet')