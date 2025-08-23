import asyncio

from ui.app import start_flet
from web_server.server import APIServer
from core.check_folder import FolderWatcher
from core.logging_config import logger


async def main():
    shutdown_event = asyncio.Event()
    watcher = FolderWatcher()
    server = APIServer()

    tasks = {
        "flet": asyncio.create_task(start_flet(shutdown_event)),
        "server": asyncio.create_task(server.start()),
        "watcher": asyncio.create_task(watcher.check_folder()),
        "shutdown": asyncio.create_task(shutdown_event.wait())
    }

    try:
        # Ждем либо shutdown_event, либо завершения любой задачи
        done, pending = await asyncio.wait(
            list(tasks.values()),
            return_when=asyncio.FIRST_COMPLETED
        )

        logger.info("Shutdown initiated")

        # Корректное завершение сервера
        await server.stop()

        # Отмена остальных задач
        for name, task in tasks.items():
            if name != "server" and not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    logger.info(f"Task {name} cancelled")
                except Exception as e:
                    logger.error(f"Error cancelling {name}: {e}")

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        raise
    finally:
        logger.info("Application shutdown completed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
    finally:
        logger.info("Process terminated")
