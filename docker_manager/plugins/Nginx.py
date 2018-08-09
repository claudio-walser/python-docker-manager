import os
import Cli
from docker_manager.plugins.AbstractPlugin import AbstractPlugin

class Nginx(AbstractPlugin):

  confd = '/etc/nginx/conf.d'

  def writeUpstreamConfig(self):
    if isinstance(self.settings['nginx']['backendPort'], list):
      for backendPort in self.settings['nginx']['backendPort']:
        if 'name' in backendPort and 'port' in backendPort:
          name = "%s-%s" % (self.name, backendPort['name'])
          self.writeConfigFile(name, self.name, self.settings['maxContainers'], backendPort['port'])
    elif isinstance(self.settings['nginx']['backendPort'], int):
      self.writeConfigFile(self.name, self.name, self.settings['maxContainers'], self.settings['nginx']['backendPort'])

    self.reload()

  def writeConfigFile(self, name, containerName, maxContainers, port):
    upstreamString = 'upstream %s {\n' % (name)
    for i in range(0, maxContainers):
      upstreamString += '    server %s-%s:%s;\n' % (containerName, i, port)
    upstreamString += '}'

    filename = '%s/upstream-%s.conf' % (self.confd, name)
    with open(filename, 'w') as f:
      f.write(upstreamString)
      f.close()

  def removeConfigFile(self, name):
    filename = '%s/upstream-%s.conf' % (self.confd, name)
    if os.path.isfile(filename):
      os.remove(filename)

  def removeUpstreamConfig(self):
    if isinstance(self.settings['nginx']['backendPort'], list):
      for backendPort in self.settings['nginx']['backendPort']:
        if 'name' in backendPort and 'port' in backendPort:
          name = "%s-%s" % (self.name, backendPort['name'])
          self.removeConfigFile(name)
    elif isinstance(self.settings['nginx']['backendPort'], int):
      self.removeConfigFile(self.name)

    self.reload()

  def reload(self):
    command = Cli.Command()
    command.execute("service nginx reload")


  # callable methods
  def start(self):
    # should optimize and do that only on creation of the container
    self.writeUpstreamConfig()
    pass

  def destroy(self):
    self.removeUpstreamConfig()
    pass
