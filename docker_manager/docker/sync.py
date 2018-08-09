

class Sync (object):
    command = CliCommand(True)
    binary = 'docker-compose'

    def start(self):
        return self.command.execute('%s start' % (self.binary))


    def stop(self):
        return self.command.execute('%s stop' % (self.binary))

