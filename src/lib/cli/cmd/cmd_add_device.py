import click
from loguru import logger
from lib.cli.app import Environment, pass_environment


@click.command("add-device", short_help="Adds a new device configuration to the app's configuration file.")
@click.argument('name', type=str)
@click.argument('host', type=str)
@click.argument('username', type=str)
@click.argument('password', type=str)
@click.argument('enabled', type=bool)
@pass_environment
def cli(ctx: Environment, name: str, host: str, username: str, password: str, enabled: bool):
    """ Adds a new device configuration to the app's configuration file. """

    logger.info(f'Adding device configuration for {name} ({host}) to {ctx.config}')

    encrypted_password: str = ctx.fernet.encrypt(password.encode()).decode('utf-8')

    config: dict[str, any] = ctx.config

    config['devices'].append({
        'name': name,
        'host': host,
        'username': username,
        'password': encrypted_password,
        'enabled': enabled,
    })

    if ctx.save_config(config):
        logger.info(f'Device configuration for {name} ({host}) added to {ctx.config}')
    else:
        logger.error(f'Failed to add device configuration for {name} ({host}) to {ctx.config}')
