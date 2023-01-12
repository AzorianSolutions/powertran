import click
from lib.cli.app import Environment, pass_environment


@click.command("add-device", short_help="Adds a new device configuration to the app's configuration file.")
@click.argument('label', type=str)
@click.argument('host', type=str)
@click.argument('username', type=str)
@click.argument('password', type=str)
@click.argument('enabled', type=bool)
@pass_environment
def cli(ctx: Environment, label: str, host: str, username: str, password: str, enabled: bool):
    """ Adds a new device configuration to the app's configuration file. """

    print(ctx.settings)

    # TODO
