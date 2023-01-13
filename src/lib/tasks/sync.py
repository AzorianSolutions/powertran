from threading import Thread
from lib.adtran.api import AdtranAPI
from lib.adtran.mutables import RemoteDevice
from lib.cli.app import Environment
from lib.mutables import Device
from lib.powercode import EquipmentShapingData


class SyncTask(Thread):
    ctx: Environment | None = None
    _device: Device | None = None

    @property
    def device(self) -> Device | None:
        """ Returns the device configuration. """
        return self._device

    @device.setter
    def device(self, device: Device | None):
        """ Sets the device to be used by the task. """
        # Decrypt the device password
        device.password = self.ctx.fernet.decrypt(device.password).decode('utf-8')
        self._device = device


class ShapingConfigTask(SyncTask):
    equipment: dict[str, EquipmentShapingData] | None = None
    dry_run: bool = False

    def run(self) -> bool:

        # Set up the Adtran API
        adtran: AdtranAPI = AdtranAPI(self.device)

        # Update the shaping configuration on the Adtran device
        adtran.update_shaping(self.equipment, self.dry_run)

        # Disconnect from the device
        adtran.close()

        return True


class DeviceSyncTask(SyncTask):
    remote_devices: list[RemoteDevice] | None = None

    def run(self) -> bool:
        """ Runs the task. """

        # Set up the Adtran API
        adtran: AdtranAPI = AdtranAPI(self.device)

        # Retrieve the list of remote devices from the Adtran device
        self.remote_devices = adtran.get_remote_devices()

        # Disconnect from the device
        adtran.close()

        return True
