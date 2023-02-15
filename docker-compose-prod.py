from os import system
from sys import argv
import yaml

secrets = yaml.safe_load(open("secrets.yaml"))
DB_PASS: str = str(secrets["database"]["password"])
DB_NAME: str = str(secrets["database"]["name"])

if len(argv) == 1 or (len(argv) == 2 and argv[1] == "up"):
    system(f"POSTGRES_PASSWORD=\"{DB_PASS}\" POSTGRES_DB=\"{DB_NAME}\" "
           f"docker-compose -f \"docker-compose-prod.yml\" up -d")
else:
    system(f"POSTGRES_PASSWORD=\"{DB_PASS}\" POSTGRES_DB=\"{DB_NAME}\" "
           f"docker-compose -f \"docker-compose-prod.yml\" down")
