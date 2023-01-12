import click
import os
import sys
from config import AppSettings

CONTEXT_SETTINGS = dict(auto_envvar_prefix="PT")


class Environment:
    _settings: AppSettings = None

    def __init__(self):
        self.project_path = os.getcwd()

    @property
    def debug(self) -> bool:
        return self._settings.debug if isinstance(self._settings, AppSettings) else False

    @debug.setter
    def debug(self, value: bool):
        if isinstance(self._settings, AppSettings):
            self._settings.debug = value

    @property
    def settings(self) -> AppSettings:
        return self._settings

    def load_settings(self, env_file: str, env_file_encoding: str, secrets_dir: str | None) -> AppSettings:
        """ Loads the app's settings from the given environment file and secrets directory. """

        if not env_file.startswith('/'):
            env_file = os.path.join(self.project_path, env_file)

        params: dict = {
            '_env_file': env_file,
            '_env_file_encoding': env_file_encoding,
        }

        os.putenv('PT_ENV_FILE', env_file)
        os.putenv('PT_ENV_FILE_ENCODING', env_file_encoding)

        if secrets_dir is not None:
            valid: bool = True
            secrets_path: str = secrets_dir if secrets_dir.startswith('/') else os.path.join(self.project_path,
                                                                                             secrets_dir)

            if not os.path.exists(secrets_path):
                valid = False
                self.log(f'The given path for the "--secrets-dir" option does not exist: {secrets_path}')
            elif not os.path.isdir(secrets_path):
                valid = False
                self.log(f'The given path for the "--secrets-dir" option is not a directory: {secrets_path}')

            if valid:
                params['_secrets_dir'] = secrets_dir
                os.putenv('PT_ENV_SECRETS_DIR', secrets_dir)

        self._settings: AppSettings = AppSettings(**params)

        return self._settings

    @staticmethod
    def log(msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.debug:
            self.log(msg, *args)


pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "cmd"))


class AsCli(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            filename = filename.lower()
            if filename.endswith('.py') and filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name: str):
        import importlib
        name = name.lower()
        try:
            mod = importlib.import_module(f'lib.cli.cmd.cmd_{name}')
        except ImportError:
            return
        return mod.cli


@click.command(cls=AsCli, context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.option(
    '-p',
    '--project-path',
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    help="Changes the project's root path.",
)
@click.option("-v", "--verbose", is_flag=True, default=None, help="Increases verbosity of the application.")
@click.option('-e', '--env-file', default='.env', type=str,
              help='The path to an .env file to load command settings from.')
@click.option('--env-file-encoding', default='UTF-8', type=str,
              help='The encoding of the env file specified by the "--env-file" option.')
@click.option('-s', '--secrets-dir', default=None, type=str,
              help='The path to a directory containing environment variable secret files.')
@pass_environment
def cli(ctx: Environment, verbose: bool | None, project_path, env_file: str, env_file_encoding: str,
        secrets_dir: str | None):
    """A CLI to consume Powertran's execution and management functions."""

    # Configure the debug setting of the application if the "--verbose" option is set.
    if isinstance(verbose, bool):
        ctx.debug = verbose

    # Cache a reference to the project's root path
    if project_path is not None:
        ctx.project_path = project_path

    # Load the app's settings based on the given options.
    ctx.load_settings(env_file, env_file_encoding, secrets_dir)
