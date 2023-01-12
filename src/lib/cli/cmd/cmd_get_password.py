import click
from loguru import logger
from lib.cli.app import Environment, pass_environment


@click.command("get-password", short_help="Retrieves the unencrypted password for a device.")
@click.argument('name', type=str)
@pass_environment
def cli(ctx: Environment, name: str):
    """ Retrieves the unencrypted password for a device. """

    target_device: dict[str, any] | None = None

    for device in ctx.config['devices']:
        if str(device['name']).lower() == name.lower():
            target_device = device
            break

    if target_device is None:
        logger.error(f'No device found with name {name}')
        return

    decrypted_password: str = ctx.fernet.decrypt(target_device['password']).decode('utf-8')

    print(f'Password for {name} ({device["host"]}): {decrypted_password}')
