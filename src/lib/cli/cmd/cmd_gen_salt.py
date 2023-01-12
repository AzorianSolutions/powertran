import click
from cryptography.fernet import Fernet
from lib.cli.app import Environment, pass_environment


@click.command("gen-salt", short_help="Generates a Fernet encryption key to be used for encrypting passwords.")
@pass_environment
def cli(ctx: Environment):
    """ Generates a Fernet encryption key to be used for encrypting passwords. """
    print(f'Generated Key: {Fernet.generate_key().decode("utf-8")}')
