from pydantic import BaseSettings


class AppSettings(BaseSettings):
    debug: bool = False
    salt: str = 'INSECURE-CHANGE-ME-;Qj^J`1i?"WuOD%Z;X-M0^CGUI>moX>twda:a=9@!=F|'
    mysql_host: str = 'localhost'
    mysql_user: str = 'root'
    mysql_password: str = ''
    mysql_database: str = 'powernoc'
    config: str = 'conf/config.yml'
    known_hosts: str = '~/.ssh/known_hosts'

    class Config:
        env_prefix = 'pt_'
