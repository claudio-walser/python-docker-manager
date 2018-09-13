import os

from simpcli import Command as CliCommand

from docker_manager.config import ComposeConfig
from docker_manager.docker.container import Container

from docker_manager.exceptions import NoDockerComposeFileException


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

  def pull(self):
    return self.comopose('pull')

  def restart(self):
    output = ''
    output += self.stop()
    output += self.start()
    return output

  def predictName(self, serviceName, service, scale = 1):
    projectName = self.name = os.path.basename(os.getcwd())

    return '%s_%s_%i' % (projectName, serviceName, scale)

  def getContainers(self):
    config = self.composeConfig.get()
    containers = []
    if 'services' in config:
      for serviceName in config['services']:
        serviceConfig = config['services'][serviceName]
        if 'container_name' in serviceConfig:
          containers.append(Container(serviceConfig['container_name'], serviceName, serviceConfig))
        else:
          if 'scale' in serviceConfig:
            for scale in range(serviceConfig['scale']):
              scale += 1
              containers.append(Container(self.predictName(serviceName, serviceConfig, scale), serviceName, serviceConfig))
          else:
            containers.append(Container(self.predictName(serviceName, serviceConfig), serviceName, serviceConfig))
    return containers
