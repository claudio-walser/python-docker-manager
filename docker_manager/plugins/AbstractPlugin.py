
class AbstractPlugin(object):

  container = None
  name = None
  settings = None

  def __init__(self, container):
    self.container = container
    self.name = self.container.getName()
    self.settings = self.container.getSettings()

  # callable methods
  def status(self):
    pass

  def start(self):
    pass

  def stop(self):
    pass

  def restart(self):
    pass

  def destroy(self):
    pass

  def update(self):
    pass
