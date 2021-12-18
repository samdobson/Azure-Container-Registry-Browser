from __future__ import annotations

import os
import re
from typing import Any, MutableMapping

import toml
from rich.console import Console
from validators.utils import validator

from . import styles
from .ask import Ask

"""
All of the good stuff. This is should be the main point for app configuration.
"""

# General
CLI_HELP = """
acr-browser is a tool for managing container images and artifacts in Azure Container Registry.
"""


@validator
def acr_name(name: str) -> bool:
    """Validate the name of the acr.

    Args:
        name (str): Name of the acr.

    Returns:
        bool: True or False depending on the name validity.
    """

    regex = "^[a-zA-Z0-9-]{3,24}$"
    pattern = re.compile(regex)
    return pattern.match(name) is not None


def set_config(path: str) -> MutableMapping[str, Any]:
    """Create a configuration file for the client.

    Args:
        path (str): Path to the configuration file.

    Returns:
        MutableMapping[str, Any]: Configuration for the client.
    """

    config = {}
    console = Console()
    ask = Ask()

    console.print(
        "It looks like this is the first time you are using this app.. lets add some configuration before we start :smiley:\n"  # noqa: E501
    )
    config["acr"] = ask.question(
        f"[b][{styles.GREY}]Container Registry Name[/][/]", validation=acr_name
    )
    with open(path, "w") as f:
        toml.dump(config, f)

    return toml.load(path)


def get_config(config: str | None = None) -> MutableMapping[str, Any]:
    """Retrieve or create configuration.

    Args:
        config (str | None): Path to the configuration file.

    Returns:
        MutableMapping[str, Any]: Configuration.
    """

    if config and os.path.exists(config):
        _config = toml.load(config)

    elif config and not os.path.exists(config):
        _config = set_config(config)

    else:
        home = os.getenv("HOME")
        config_path = f"{home}/.acr-browser.toml"

        if not os.path.exists(config_path):
            _config = set_config(config_path)
        else:
            _config = toml.load(config_path)

    return _config