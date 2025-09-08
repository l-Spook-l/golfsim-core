import os
import json

import aiofiles
from core.logging_config import logger


SETTINGS_FILE = "settings.json"


async def load_settings() -> dict:
    """
    Loads settings from the settings.json file.

    Returns:
        dict: Dictionary with settings. Empty if the file is missing, empty, or corrupted.
    """
    data = {}

    if not os.path.exists(SETTINGS_FILE):
        logger.info(f"File {SETTINGS_FILE} not  found.")
        return data

    try:
        async with aiofiles.open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            content = await f.read()
            if not content.strip():
                return data
            data = json.loads(content)
    except json.JSONDecodeError:
        logger.warning("Settings file is corrupted or contains invalid JSON. Creating a new one.")
    except Exception as e:
        logger.error(f"Error reading the settings file: {e}")

    return data
