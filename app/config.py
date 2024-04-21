import json
from pydantic_settings import BaseSettings

conf_filepath = 'config/db_conf.json'

class Settings(BaseSettings):
    db_hostname: str
    db_name: str
    db_username: str
    db_pwd: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

def read_config(file_path: str) -> dict:
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def create_settings_from_config(file_path: str) -> Settings:
    config = read_config(file_path)

    return Settings(**config)

settings = create_settings_from_config(conf_filepath)

