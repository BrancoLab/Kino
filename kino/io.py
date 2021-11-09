# type: ignore

from pathlib import Path
from typing import Union

import json
import yaml

# -------------------------------- decorators -------------------------------- #


def raise_on_path_not_exists(func):
    """
        Decorator that raises an error when the
        path passed to a function does not point towards an actual file
    """

    def inner(*args, **kwargs):
        args = list(args)
        path = args[0]
        if not path.exists():
            raise FileNotFoundError(f"File or folder: {path} does not exist")
        else:
            return func(*args, **kwargs)

    return inner


def pathify(func):
    """ 
        Decorator that makes sure that the first arugment to a function
        is a Path object and not a path as string
    """

    def inner(*args, **kwargs):
        args = list(args)
        args[0] = Path(args[0])
        return func(*args, **kwargs)

    return inner


# ---------------------------------- saving ---------------------------------- #


@pathify
def to_json(filepath: Union[str, Path], obj: dict):
    """ saves an object to json """
    if isinstance(obj, str):
        obj = json.loads(obj, indent=4, sort_keys=True)

    with open(filepath, "w") as out:
        json.dump(obj, out, indent=4, sort_keys=True)


@pathify
def to_yaml(filepath: Union[str, Path], obj: dict):
    """ saves an object to yaml """
    with open(filepath, "w") as out:
        yaml.dump(obj, out, default_flow_style=False, indent=4)


# ---------------------------------- loading --------------------------------- #
@pathify
@raise_on_path_not_exists
def from_json(filepath: Union[str, Path]) -> dict:
    """ loads an object from json """
    with open(filepath, "r") as fin:
        return json.load(fin)


@pathify
@raise_on_path_not_exists
def from_yaml(filepath: Union[str, Path]) -> dict:
    """ loads an object from yaml """
    with open(filepath, "r") as fin:
        return yaml.load(fin, Loader=yaml.FullLoader)
