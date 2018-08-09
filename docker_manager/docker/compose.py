from simpcli import Command as CliCommand
from simpcli import Interface as CliInterface


class Compose (object):

  command = CliCommand(True)
  composeCommand = 'docker-compose'

  def comopose(self, command, service = ''):
    if service == 'all-services':
      service = ''
    return self.command.execute('%s %s %s' % (self.composeCommand, command, service))

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