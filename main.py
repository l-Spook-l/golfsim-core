"""
Main entry point for the GolfSim application.

Responsible for initializing the database, starting the Flet UI,
FastAPI web server, and the folder watcher. Manages the
application lifecycle and ensures proper termination of all tasks.
"""

import asyncio

from ui.app import start_flet
from web_server.server import APIServer
from data_base.config_db import run_migrations, DB_FILE
from core.check_folder import FolderWatcher
from core.logging_config import logger


async def main():
    """
    Main coroutine of the application.

    Runs three parallel tasks:
        - Flet UI (`start_flet`)
        - Web server (`APIServer.start`)
        - Folder watcher (`FolderWatcher.check_folder`)

    It also waits for a shutdown event (`shutdown_event`) and
    properly stops the server and cancels the remaining tasks.

    Raises:
        Any unhandled errors are logged and re-raised.
    """
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
        # Wait for either the shutdown_event or the completion of any task
        done, pending = await asyncio.wait(
            list(tasks.values()),
            return_when=asyncio.FIRST_COMPLETED
        )

        logger.info("Shutdown initiated")

        # Graceful server shutdown
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
        if not DB_FILE.exists():
            run_migrations()
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
    finally:
        logger.info("Process terminated")
