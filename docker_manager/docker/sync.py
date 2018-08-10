from simpcli import Command as CliCommand


class Sync (object):
    command = CliCommand(True)
    binary = 'docker-sync'

    def start(self):
        return self.command.execute('%s start' % (self.binary))

    def stop(self):
        return self.command.execute('%s stop' % (self.binary))

    def destroy(self):
        return self.command.execute('%s clean' % (self.binary))