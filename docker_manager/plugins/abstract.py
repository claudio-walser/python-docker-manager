
class BasePlugin(object):

  container = None
  name = None
  settings = None

  #def __init__(self, container):
  def run(self, command, container):
    if hasattr(self, command):
        self.container = container
        print(self.container.getName())
        print(self.container.getServiceName())
        print(self.container.getServiceConfig())
        func = getattr(self, command)
        func()