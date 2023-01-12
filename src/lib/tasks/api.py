from loguru import logger
from lib.powercode import EquipmentShapingData
from lib.tasks.sync import ShapingConfigTask


class TaskAPI:
    _tasks: dict[str, list[ShapingConfigTask]] = {
        'sync': [],
    }

    @staticmethod
    def run_sync_task(config: dict[str, any], equipment: dict[str, EquipmentShapingData],
                      dry_run: bool = False) -> bool:
        """ Runs the shaping configuration synchronization task. """

        # Instantiate a task for each configured Adtran device and start the task
        for device in config['devices']:

            # Skip disabled devices
            if not device['enabled']:
                logger.debug(f"Skipping device '{device['name']}' because it is disabled.")
                continue

            logger.debug('Starting shaping configuration synchronization task for device: ' + device['name'])
            
            # Instantiate a task for the device
            task: ShapingConfigTask = ShapingConfigTask()
            task.device = device
            task.equipment = equipment
            task.dry_run = dry_run
            TaskAPI._tasks['sync'].append(task)
            task.start()

        # Wait for all tasks to complete
        for task in list[ShapingConfigTask](TaskAPI._tasks['sync']):
            task.join()

        return True
