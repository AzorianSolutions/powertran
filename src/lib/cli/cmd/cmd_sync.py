import click
from loguru import logger
from lib.adtran.api import AdtranAPI
from lib.cli.app import Environment, pass_environment
from lib.powercode import EquipmentShapingData, PowercodeAPI


@click.command("sync", short_help="Runs the synchronization process from Powercode to the configured Adtran devices.")
@click.option('-d', '--dryrun', is_flag=True, default=False)
@pass_environment
def cli(ctx: Environment, dryrun: bool):
    """ Runs the synchronization process from Powercode to the configured Adtran devices. """

    # Load the equipment shaping data from Powercode database
    equipment: dict[str, EquipmentShapingData] = PowercodeAPI.get_equipment_shaping_data()

    # Set up the Adtran API
    adtran: AdtranAPI = AdtranAPI()

    # Update the shaping configuration on the Adtran device
    result: str = adtran.update_shaping(equipment, dryrun)

    print(result)

    # Disconnect from the device
    adtran.close()

    logger.success('Shaping configuration applied successfully!')
