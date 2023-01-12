from threading import Thread
from lib.adtran.api import AdtranAPI
from lib.cli.app import Environment
from lib.powercode import EquipmentShapingData


class ShapingConfigTask(Thread):

    ctx: Environment | None = None
    device: dict[str, any] | None = None
    equipment: dict[str, EquipmentShapingData] | None = None
    dry_run: bool = False

    def run(self) -> bool:

        # Decrypt the device password
        self.device['password'] = self.ctx.fernet.decrypt(self.device['password']).decode('utf-8')

        # Set up the Adtran API
        adtran: AdtranAPI = AdtranAPI(self.device)

        # Update the shaping configuration on the Adtran device
        adtran.update_shaping(self.equipment, self.dry_run)

        # Disconnect from the device
        adtran.close()

        return True
