import asyncio

from gui.app import start_flet  # Импортируем функцию для запуска Flet
from web_server.server import start_server  # Импортируем функцию для запуска FastAPI сервера
from check_folder import check_folder_main


async def main():
    await asyncio.gather(
        start_server(),
        start_flet(),
        check_folder_main(),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Приложение остановлено")
