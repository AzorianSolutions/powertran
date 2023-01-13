from threading import Thread
from lib.adtran.api import AdtranAPI
from lib.adtran.mutables import RemoteDevice
from lib.cli.app import Environment
from lib.mutables import Device
from lib.powercode import EquipmentShapingData


class SyncTask(Thread):
    """ A base class for synchronizing configuration on a device. """
    ctx: Environment | None = None
    device: Device | None = None


class ShapingConfigTask(SyncTask):
    """ A task for synchronizing shaping configuration. """
    equipment: dict[str, EquipmentShapingData] | None = None
    dry_run: bool = False

    def run(self) -> bool:
        """ Runs the shaping configuration synchronization task. """

        # Set up the Adtran API
        adtran: AdtranAPI = AdtranAPI(self.device)

        # Update the shaping configuration on the Adtran device
        adtran.update_shaping(self.equipment, self.dry_run)

        # Disconnect from the device
        adtran.close()

        return True


class DeviceSyncTask(SyncTask):
    """ A task for synchronizing device configuration. """
    remote_devices: list[RemoteDevice] | None = None

    def run(self) -> bool:
        """ Runs the remote device information synchronization task. """

        # Set up the Adtran API
        adtran: AdtranAPI = AdtranAPI(self.device)

        # Retrieve the list of remote devices from the Adtran device
        self.remote_devices = adtran.get_remote_devices()

        # Disconnect from the device
        adtran.close()

        return True
