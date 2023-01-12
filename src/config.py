from pydantic import BaseSettings


class AppSettings(BaseSettings):
    debug: bool = False
    salt: str = 'WXQVPexFCGZmKfHkFjiW0lhrAC2XJ8K8Gm7wK9HYGxE='
    mysql_host: str = 'localhost'
    mysql_user: str = 'root'
    mysql_password: str = ''
    mysql_database: str = 'powernoc'
    config: str = 'conf/config.yml'
    known_hosts: str = '~/.ssh/known_hosts'

    class Config:
        env_prefix = 'pt_'
