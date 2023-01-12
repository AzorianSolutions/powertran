from loguru import logger
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

    def execute(self, commands: str | list[str], dry_run: bool = False) -> str:
        """ Execute a command on the device. """

        if dry_run:
            logger.debug(f'Dry run mode, not sending commands to device.')
            print(commands)
            return ''

        return self._client.execute(commands)

    def close(self):
        """ Close the SSH connection to the device. """
        self._client.close()

    def get_remote_devices(self) -> list[RemoteDevice]:
        """ Get a list of RemoteDevice objects from the device. """
        return AdtranUtil.parse_remote_device_list(
            self._client.execute('show table remote-devices ont')
        )
