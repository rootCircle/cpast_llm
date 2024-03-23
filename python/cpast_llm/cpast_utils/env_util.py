import os
from langchain_core.pydantic_v1 import SecretStr


class MissingEnvironmentVariable(Exception):
    pass


def get_env_var(var_name: str) -> SecretStr:
    try:
        return SecretStr(os.environ[var_name])
    except KeyError as err:
        raise MissingEnvironmentVariable(f'{var_name} does not exist') from err
