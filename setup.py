from setuptools import setup

setup(
    name='powertran',
    version='0.1.0',
    package_dir={'': 'src'},
    install_requires=[
        'click==8.1.3',
        'dotenv-cli==3.1.0',
        'python-dotenv==0.21.0',
        'loguru==0.6.0',
        'pydantic==1.10.4',
        'ssh-python==1.0.0',
        'paramiko==2.12.0',
        'netmiko==4.1.2',
        'mysqlclient==2.1.1',
        'pyaml==21.10.1',
        'cryptography==39.0.0',
    ],
    entry_points={
        'console_scripts': [
            'powertran = lib.cli.app:cli',
        ],
    },
)
