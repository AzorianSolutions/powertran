import click
from loguru import logger
from lib.cli.app import Environment, pass_environment
from lib.powercode import EquipmentShapingData, PowercodeAPI
from lib.tasks.api import TaskAPI


@click.command("sync", short_help="Runs the synchronization process from Powercode to the configured Adtran devices.")
@click.option('-d', '--dryrun', is_flag=True, default=False)
@pass_environment
def cli(ctx: Environment, dryrun: bool):
    """ Runs the synchronization process from Powercode to the configured Adtran devices. """

    # Load the equipment shaping data from Powercode database
    equipment: dict[str, EquipmentShapingData] = PowercodeAPI.get_equipment_shaping_data()

    # Start a synchronization task for each device
    TaskAPI.run_sync_task(ctx, equipment, dryrun)

    logger.success('Shaping configuration applied successfully!')
