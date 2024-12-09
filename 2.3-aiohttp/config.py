import os

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "aioapi")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "0.0.0.0")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")