# config.py
# Reference: https://www.fastapitutorial.com/blog/fastapi-hello-world/
import logging
import os
import sys


class LogConfig:
    logger = logging.getLogger("app_log")
    logger.setLevel(logging.INFO)  # Set the logging level (DEBUG, INFO, etc.)

    # Create a StreamHandler to log to stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)  # Set the handler's logging level

    # Define a log format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(stream_handler)


class Settings:
    PROJECT_NAME: str = "MBdgt"
    PROJECT_VERSION: str = "1.0.0"
    POSTGRES_PORT = 5432
    POSTGRES_USER: str = "appuser"
    POSTGRES_DB: str = os.environ.get("DATABASE_PWD", "app")
    POSTGRES_PASSWORD: str = os.environ.get("DATABASE_PWD", "supersecretpassword")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", "localhost")
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "skufhoweiu098ye879yih")  # new
    ALGORITHM = "HS256"  # new
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins  #new


"""docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres"""
settings = Settings()
log = LogConfig.logger
