from loguru import logger
from lib.adtran.mutables import RemoteDevice
from lib.adtran.util import AdtranUtil
from lib.mutables import Device
from lib.powercode import EquipmentShapingData
from lib.ssh.client import SSHClientManager


class AdtranAPI:
    """ A class for interacting with Adtran devices. """

    _device: Device | None = None
    _client: SSHClientManager = None
    _client_conf: dict[str, any] | None = None

    def __init__(self, device: Device | None = None, auto_connect: bool = True):
        """ Initialize the AdtranAPI object. """

        if isinstance(device, Device):
            self._device = device
            self._client_conf = {key: value for key, value in self._device.__dict__.items() if
                                 key in ['host', 'port', 'username', 'password']}
            self._client_conf['password'] = self._device.decrypted_password

        if auto_connect:
            self.open()

    def open(self):
        """ Open an SSH connection to the device. """
        if not isinstance(self._client, SSHClientManager):
            self._client = SSHClientManager(**self._client_conf, auto_connect=True)

    def close(self):
        """ Close the SSH connection to the device. """
        self._client.close()

    def execute(self, commands: str | list[str], dry_run: bool = False) -> str:
        """ Execute a command on the device. """

        if dry_run:
            logger.debug(f'Dry run mode, not sending commands to device.')

            if isinstance(commands, str):
                commands = [commands]

            for command in commands:
                print(command)

            return ''

        return self._client.execute(commands)

    def get_remote_devices(self) -> list[RemoteDevice]:
        """ Get a list of RemoteDevice objects from the device. """
        return AdtranUtil.parse_remote_device_list(
            self._client.execute(['enable', 'show table remote-devices ont'])
        )

    def update_shaping(self, equipment: dict[str, EquipmentShapingData], dry_run: bool = False) -> str:
        """ Update the shaping configuration on the Adtran device. """

        logger.info('Building shaping configuration for Adtran OLT device.')

        # Query the Adtran device for the current remote device list for ONTs and parse the results
        devices = self.get_remote_devices()

        # Build shaping configuration command buffer
        commands: list[str] = AdtranUtil.build_shaping_buffer(equipment, devices)

        logger.info('Applying shaping configuration to Adtran OLT device.')

        # Execute the command buffer
        return self.execute(commands, dry_run)
