import re
import os

from docker_manager.plugins.abstract import BasePlugin

from docker_manager.exceptions import HostfileNotWritableException

class Hosts(BasePlugin):

  hostsFile = '/etc/hosts'
  name = 'Hosts Plugin'
  description = 'Writing hosts file for container %s'

  def __init__(self):
    if not os.access(self.hostsFile, os.W_OK):
      raise HostfileNotWritableException('Check that your hostsfile %s is writeable under your current user!' % (self.hostsFile))

  def add(self, ip, hostname):
    with open(self.hostsFile, 'r+') as f:
      hostsfile = f.read()
      if hostsfile.find(hostname) is not -1:
        hostsfile = re.sub(r"\n(.*)    %s\n" % hostname, "\n%s    %s\n" % (ip, hostname), hostsfile)
      else:
        hostsfile += "%s    %s\n" % (ip, hostname)
      f.seek(0)
      f.write(hostsfile)
      f.truncate()

  def remove(self, hostname):
    with open(self.hostsFile, 'r+') as f:
      hostsfile = f.read()
      if hostsfile.find(hostname) is not -1:
        hostsfile = re.sub(r"\n(.*)    %s\n" % hostname, "\n", hostsfile)
      f.seek(0)
      f.write(hostsfile)
      f.truncate()


  def getConfig(self):
    config = self.config.get()
    if 'services' in config:
      if self.container.getServiceName() in config['services']:
        if 'hosts' in config['services'][self.container.getServiceName()]:
          aliases = config['services'][self.container.getServiceName()]['hosts']
          aliases.append(self.container.getName())
          return aliases

    return False

  # callable methods
  def start(self):
    aliases = self.getConfig()
    if not aliases:
      return False

    self.add(self.container.getIpAddress(), ' '.join(aliases))
    return True

  def stop(self):
    aliases = self.getConfig()
    if not aliases:
      return False

    self.remove(' '.join(aliases))
    return True

  def restart(self):
    self.stop()
    self.start()
    pass

  def destroy(self):
    self.stop()
    pass

  def update(self):
    self.stop()
    self.start()
    pass