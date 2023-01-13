import multiprocessing

from loguru import logger
from multiprocessing import Pool
from lib.adtran.api import AdtranAPI
from lib.adtran.mutables import RemoteDevice
from lib.adtran.util import AdtranUtil
from lib.cli.app import Environment
from lib.powercode import EquipmentShapingData
from lib.tasks.sync import SyncTask, DeviceSyncTask


class TaskAPI:
    """ Task API. """

    _ctx: Environment | None = None
    _equipment: dict[str, EquipmentShapingData] | None = None
    _dry_run: bool = False
    _tasks: dict[str, list[SyncTask]] = {
        'device_sync': [],
    }
    _remote_devices: dict[str, list[RemoteDevice]] = {}
    _command_sets: list[tuple[str, list[str]]] = []
    _apis: dict[str, AdtranAPI] = {}

    @property
    def ctx(self) -> Environment | None:
        """ Returns the CLI context. """
        return self._ctx

    @property
    def equipment(self) -> dict[str, EquipmentShapingData] | None:
        """ Returns the equipment shaping data. """
        return self._equipment

    @property
    def dry_run(self) -> bool:
        """ Returns the dry run flag. """
        return self._dry_run

    @property
    def remote_devices(self) -> dict[str, list[RemoteDevice]]:
        """ Returns the remote devices. """
        return self._remote_devices

    def __init__(self, ctx: Environment, equipment: dict[str, EquipmentShapingData],
                 dry_run: bool = False):
        self._ctx = ctx
        self._equipment = equipment
        self._dry_run = dry_run

    def run_sync_task(self) -> bool:
        """ Runs the shaping configuration synchronization task. """

        # Instantiate a task for each configured Adtran device and start the task
        for device in self.ctx.devices:
            # Skip disabled devices
            if not device.enabled:
                logger.debug(f"Skipping device '{device.name}' because it is disabled.")
                continue

            logger.debug('Starting shaping configuration synchronization task for device: '
                         + device.name if isinstance(device.name, str) else device.host)

            # Instantiate a task for the device
            task: DeviceSyncTask = DeviceSyncTask()
            task.ctx = self.ctx
            task.device = device
            task.dry_run = self.dry_run
            self._tasks['device_sync'].append(task)
            task.start()

        total_remote_devices: int = 0

        # Wait for all tasks to complete
        for task in list[DeviceSyncTask](self._tasks['device_sync']):
            task.join()

            if task.device.host not in self._remote_devices:
                self._remote_devices[task.device.host] = []

            total_remote_devices += len(task.remote_devices)

            self._remote_devices[task.device.host].extend(task.remote_devices)

        logger.info(f'Loaded {total_remote_devices} remote devices across {len(self._remote_devices)} devices.')

        # Build the shaping configuration queue
        self.build_queue()

        threads: int = int(self.ctx.config['threading']['pool_size'])

        logger.info(f'Processing shaping configuration queue with {threads} threads.')

        pool = Pool(threads)
        pool.starmap(self.queue_worker, self._command_sets)

        logger.info(f'Finished shaping configuration synchronization task for {len(self._command_sets)} devices.')

        return True

    def build_queue(self):
        """ Builds the shaping configuration queue. """

        # Iterate over the remote devices
        for host, devices in self.remote_devices.items():
            for device in list[RemoteDevice](devices):
                # Build shaping configuration command buffer
                command_set: list[str] | None = AdtranUtil.build_shaping_command(self.equipment, device)

                # Add the command set to the queue
                if isinstance(command_set, list):
                    self._command_sets.append((host, command_set))

    def queue_worker(self, host: str, command_set: list[str]):
        """ Worker function for the shaping configuration queue. """
        import random
        import time

        # Instantiate an API for each managed device if not already setup
        if not len(self._apis) == len(self.ctx.devices):
            for device in self.ctx.devices:
                if device.host not in self._apis:
                    time.sleep(random.randint(3, 10))
                    self._apis[device.host] = AdtranAPI(device)
                    self._apis[device.host].execute(['enable', 'config t'])

        # Update the shaping configuration on the Adtran device
        self._apis[host].execute(command_set, self.dry_run)
