import os
import json

import aiofiles
from core.logging_config import logger


async def load_settings() -> dict:
    data = {}
    if os.path.exists("settings.json"):
        async with aiofiles.open("settings.json", "r", encoding="utf-8") as f:
            try:
                content = await f.read()
                if content.strip():
                    data = json.loads(content)
                else:
                    logger.info("Файл пустой. Создаём заново.")
            except json.JSONDecodeError:
                logger.info("Файл повреждён. Создаём заново.")

    return data
