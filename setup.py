from setuptools import setup

setup(
    name='powertran',
    version='0.1.0',
    package_dir={'': 'src'},
    install_requires=[
        'ssh-python==1.0.0',
        'paramiko==2.12.0',
    ],
)
