from __future__ import annotations

import json

from copy import deepcopy
from shutil import move
from tempfile import NamedTemporaryFile
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from flockwave.app_framework.configurator import Configuration
    from flockwave.server.app import SkybrushServer

__all__ = (
    "can_save_server_configuration",
    "get_server_configuration_as_json",
    "save_server_configuration",
)


def get_server_configuration_as_json(
    app: "SkybrushServer", *, compact: bool = False
) -> "Configuration":
    """Returns the entire configuration of the server application as a JSON
    object. This may be used for debugging purposes if we want a full snapshot
    that contains the configuration of all the loaded extensions.

    Parameters:
        app: the server application
        compact: whether to return a compact representation that includes only
            the differences from the base configuration of the server
    """
    config: "Configuration"
    defaults: "Configuration"

    config = deepcopy(app.configurator.result)

    if compact:
        # Figure out what the defaults were
        if app.configurator.loaded_files:
            defaults = app.configurator.loaded_files[0].pre_snapshot
        else:
            defaults = deepcopy(config)
    else:
        defaults = {}

    # Extension configurations might have been modified by the user so update
    # those from the extension manager
    ext_configs = app.extension_manager.get_configuration_snapshot_dict(
        disable_unloaded=True
    )
    config["EXTENSIONS"] = ext_configs

    # If the user requested a compact representation, compare the defaults with
    # the current configuration
    if compact:
        app.configurator.minimize_configuration(config, defaults)

        # minimize_configuration() leaves empty dicts for extensions that are
        # currently loaded but all their settings are identical to the defaults.
        # We can safely remove those extension that are loaded only because
        # other extensions depend on them.
        if "EXTENSIONS" in config:
            ext_configs = config["EXTENSIONS"]
            default_ext_configs = defaults["EXTENSIONS"]

            leaf_exts = app.extension_manager.loaded_leaf_extensions

            for key in list(ext_configs.keys()):
                value = ext_configs[key]
                if isinstance(value, dict) and key not in leaf_exts:
                    should_delete = not value
                    if not should_delete:
                        # If the extension is disabled, but it was also disabled
                        # in the defaults, and there are no other changes, we can
                        # remove it from the dict
                        if value == {"enabled": False}:
                            if (
                                key not in default_ext_configs
                                or not default_ext_configs[key].get("enabled", True)
                            ):
                                should_delete = True
                    if should_delete:
                        del ext_configs[key]

    return config


def can_save_server_configuration(app: Optional["SkybrushServer"]) -> bool:
    """Returns whether it is possible to save the current configuration of the
    server back into a configuration file.
    """
    if not app:
        return False

    loaded_files = app.configurator.loaded_files
    if not loaded_files:
        return False

    last_loaded_file = loaded_files[-1]
    if not str(last_loaded_file.format.value).startswith("json"):
        return False

    return True


async def save_server_configuration(app: "SkybrushServer") -> bool:
    """Saves the current configuration of the server application, overwriting
    the configuration file that was loaded the last time.
    """
    if not can_save_server_configuration(app):
        return False

    last_loaded_file = app.configurator.loaded_files[-1]
    config = get_server_configuration_as_json(app, compact=True)

    tmpfile = NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".cfg", delete=False
    )
    with tmpfile as fp:
        json.dump(config, fp, indent=2, sort_keys=True)

    move(tmpfile.name, last_loaded_file.name)
    return True
