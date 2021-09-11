"""
    Main logger module
"""
import os
import json
import logging.config

import logging

def setup_logging(
        config_file: str, default_level: int = logging.INFO, env_key: str = "LOG_CFG"
):
    """
    Setting up loggin config
    """
    # setup logging configuration

    config_file = os.getenv(env_key, config_file)

    if os.path.exists(config_file):
        try:
            with open(config_file, "rt") as file_handler:
                config = json.load(file_handler)
            logging.config.dictConfig(config)
            return
        except Exception:
            # pylint: disable=C0415
            import traceback

            traceback.print_exc()

    logging.basicConfig(level=default_level)
