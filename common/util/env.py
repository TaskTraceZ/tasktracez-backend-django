import os
from typing import Dict

from dotenv import load_dotenv


load_dotenv()


def get_env_vars(*args: str) -> Dict[str, str]:
    env_vars = {}

    for arg in args:
        env_vars[arg] = os.getenv(arg)

        if not env_vars[arg]:
            raise EnvironmentError(f"'{arg}'")

    return env_vars


def get_env_var(var: str) -> str:
    value = os.getenv(var)

    if not value:
        raise EnvironmentError(f"'{var}")
    
    return value
