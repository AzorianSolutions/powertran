import click
from loguru import logger
from ncclient import manager
from lib.cli.app import Environment, pass_environment
from lib.powercode import EquipmentShapingData, PowercodeAPI
from lib.tasks.api import TaskAPI


@click.command("test", short_help="Runs test code.")
@click.option('-d', '--dryrun', is_flag=True, default=False)
@pass_environment
def cli(ctx: Environment, dryrun: bool):
    """ Runs test code. """

    for device in ctx.devices:
        # Skip disabled devices
        if not device.enabled:
            logger.debug(f"Skipping device '{device.name}' because it is disabled.")
            continue

        logger.debug('Starting shaping configuration synchronization task for device: '
                     + device.name if isinstance(device.name, str) else device.host)

        with manager.connect(host=device.host, port=830, username=device.username, hostkey_verify=False) as m:
            c = m.get_config(source='running').data_xml
            with open("%s.xml" % device.host, 'w') as f:
                f.write(c)
