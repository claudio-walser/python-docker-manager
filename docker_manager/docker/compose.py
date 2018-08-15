import os

from simpcli import Command as CliCommand

from docker_manager.config import ComposeConfig

from docker_manager.exceptions import NoDockerComposeFileException

from pprint import pprint


class Compose (object):

  command = CliCommand(True)
  binary = 'docker-compose'
  dockerBinary = 'docker'
  composeConfig = None

  def __init__(self):
    composeFile = './docker-compose.yml'
    if not os.path.isfile(composeFile):
        raise NoDockerComposeFileException("No docker-compose.yaml found in %s!" % os.getcwd())
    self.composeConfig = ComposeConfig()
    self.composeConfig.load()

  def comopose(self, command, service = ''):
    if service == 'all-services':
      service = ''
    return self.command.execute('%s %s %s' % (self.binary, command, service))

  def start(self):
    config = self.composeConfig.get()
    if 'volumes' in config:
      for vol in config['volumes']:
        volume = config['volumes'][vol]
        if 'external' in volume and volume['external'] == True:
          self.command.execute('%s volume create %s' % (self.dockerBinary, vol))

    return self.comopose('up -d')

  def stop(self):
    return self.comopose('stop')

  def kill(self):
    return self.comopose('kill')

  def status(self):
    return self.comopose('top')

  def destroy(self):
    self.kill()
    return self.comopose('rm -f')

  def update(self):
    return self.comopose('update')

  def restart(self):
    output = ''
    output += self.stop()
    output += self.start()
    return output

  def predictName(self, serviceIndex, service, scale = 1):
    projectName = self.name = os.path.basename(os.getcwd())

    return '%s_%s_%i' % (projectName, serviceIndex, scale)

  def getContainerNames(self):
    config = self.composeConfig.get()
    containerNames = []
    if 'services' in config:
      for serviceIndex in config['services']:
        service = config['services'][serviceIndex]
        if 'container_name' in service:
          containerNames.append(service['container_name'])
        else:
          if 'scale' in service:
            for scale in range(service['scale']):
              scale += 1
              containerNames.append(self.predictName(serviceIndex, service, scale))
          else:
            containerNames.append(self.predictName(serviceIndex, service))
    return containerNames
