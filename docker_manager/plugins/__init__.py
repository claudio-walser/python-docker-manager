from docker_manager.config import ComposeExtendedConfig
from pprint import pprint

class BasePlugin(object):

  container = None
  name = None
  settings = None

  #def __init__(self, container): 
  def run(self, command, container):
    if hasattr(self, command):
        self.container = container
        self.config = ComposeExtendedConfig()
        self.config.load()
        # print(self.container.getName())
        # print(self.container.getServiceName())
        # print(self.container.getServiceConfig())
        func = getattr(self, command)
        return func()

    return False, ''