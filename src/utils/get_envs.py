import os

from dotenv import dotenv_values


def envs():
    return {
        **dotenv_values(".env"),
        **os.environ
    }






