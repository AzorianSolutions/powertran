from lib.adtran.mutables import RemoteDevice
from lib.adtran.util import AdtranUtil
from lib.ssh.client import SSHClientManager


class AdtranAPI:
    """ A class for interacting with Adtran devices. """

    _client: SSHClientManager = None

    def __init__(self):
        """ Initialize the AdtranAPI object. """
        self._client = SSHClientManager(auto_connect=True)
        self._client.execute('enable')

    def execute(self, commands: str | list[str]) -> str:
        """ Execute a command on the device. """
        if isinstance(commands, list):
            commands = '\r'.join(commands)
        return self._client.execute(commands)

    def close(self):
        """ Close the SSH connection to the device. """
        self._client.close()

    def get_remote_devices(self) -> list[RemoteDevice]:
        """ Get a list of RemoteDevice objects from the device. """
        return AdtranUtil.parse_remote_device_list(
            self._client.execute('show table remote-devices ont', True)
        )
