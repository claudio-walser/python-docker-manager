import json

from simpcli import Command as CliCommand


class Container(object):


  id = None
  name = None
  serviceName = None
  serviceConfig = None
  running = False
  created = False
  settings = {}
  dockerSettings = {}
  interface = None
  command = CliCommand()
  waitedForIp = 0
  waitForIpMax = 20

  def __init__(self, name, serviceName, serviceConfig):
    self.name = name
    self.serviceName = serviceName
    self.serviceConfig = serviceConfig
    id = self.getId()
    if id is not None:
      self.created = True
      self.inspect()

  def inspect(self):
    output = self.command.execute("docker inspect %s" % self.id)
    if output is False:
      return False
    self.dockerSettings = json.loads(output)[0]
    self.running = self.dockerSettings['State']['Running']

  def getName(self):
    return self.name

  def getServiceName(self):
    return self.serviceName

  def getServiceConfig(self):
    return self.serviceConfig

  def getIpAddress(self):
    if self.running:
      ipAddress = self.dockerSettings['NetworkSettings']['IPAddress']
      if ipAddress == '':
      	for network in self.dockerSettings['NetworkSettings']['Networks']:
      		network = self.dockerSettings['NetworkSettings']['Networks'][network]
      		if 'IPAddress' in network:
      			ipAddress = network['IPAddress']
      			return ipAddress
      return ipAddress

  def getId(self):
    if self.id:
      return self.id

    output = self.command.execute('docker ps -aqf "name=%s"' % self.name)
    if output == '':
      return None

    self.id = output
    return self.id

  def isRunning(self):
    return self.running

  def isCreated(self):
    return self.created


  def waitForIp(self):
    self.waitedForIp += 1
    if self.waitedForIp >= self.waitForIpMax:
      return False

    self.inspect()
    if self.getIpAddress() is None:

      return self.waitForIp()

    return True
