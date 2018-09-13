import re
import os

from docker_manager.plugins import BasePlugin

from docker_manager.exceptions import HostfileNotWritableException


class Hosts(BasePlugin):

  hostsFile = '/etc/hosts'
  name = 'Hosts Plugin'

  def checkFileAccess(self):
    if not os.access(self.hostsFile, os.W_OK):
      raise HostfileNotWritableException('Check that your hostsfile %s is writeable under your current user!' % (self.hostsFile))

  def add(self, ip, hostname):
    message = 'Nothing to do'
    self.checkFileAccess()
    with open(self.hostsFile, 'r+') as f:
      hostsfile = f.read()
      if hostsfile.find(hostname) is not -1:
        hostsfile = re.sub(r"\n(.*)    %s\n" % hostname, "\n%s    %s\n" % (ip, hostname), hostsfile)
        message = 'Update hosts file:  %s' % (hostname)
      else:
        hostsfile += "%s    %s\n" % (ip, hostname)
        message = 'Add to hosts file:  %s' % (hostname)
      f.seek(0)
      f.write(hostsfile)
      f.truncate()
      return message

  def remove(self, hostname):
    message = 'Nothing to do'
    self.checkFileAccess()
    with open(self.hostsFile, 'r+') as f:
      hostsfile = f.read()
      if hostsfile.find(hostname) is not -1:
        hostsfile = re.sub(r"\n(.*)    %s\n" % hostname, "\n", hostsfile)
        message = 'Remove from hosts file:  %s' % (hostname)
      f.seek(0)
      f.write(hostsfile)
      f.truncate()
      return message


  def getAliases(self):
    config = self.config.get()
    if 'services' in config:
      if self.container.getServiceName() in config['services']:
        if config['services'][self.container.getServiceName()] and 'hosts' in config['services'][self.container.getServiceName()]:
          aliases = config['services'][self.container.getServiceName()]['hosts']
          aliases.append(self.container.getName())
          return aliases

    return []

  # callable methods
  def start(self):
    aliases = self.getAliases()
    if not aliases:
      return False, ''

    message = self.add(self.container.getIpAddress(), ' '.join(aliases))
    return True, message

  def stop(self):
    aliases = self.getAliases()
    if not aliases:
      return False, ''

    message = self.remove(' '.join(aliases))
    return True, message

  def restart(self):
    return self.start()

  def destroy(self):
    return self.stop()

  def update(self):
    return self.start()