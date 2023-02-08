from pydantic import BaseSettings
from os.path import dirname, realpath, join
import yaml


base_dir = dirname(dirname(realpath(__file__)))
secrets = yaml.safe_load(open(join(base_dir, "secrets.yaml")))


class Settings(BaseSettings):
    DB_USER: str = str(secrets["database"]["user"])
    DB_PASS: str = str(secrets["database"]["password"])
    DB_IP: str = str(secrets["database"]["ip"])
    DB_NAME: str = str(secrets["database"]["name"])
    DB_PORT: str = str(secrets["database"]["port"])
    SECRET_KEY: str = str(secrets["oauth2"]["secret_key"])
    ALGORITHM: str = str(secrets["oauth2"]["algorithm"])
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(secrets["oauth2"]["access_token_expire_minutes"])


settings = Settings()
