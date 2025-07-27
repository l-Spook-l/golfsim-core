import os
import asyncio

from find_ball import find_golf_ball
from logging_config import logger


class FolderWatcher:
    def __init__(self, directory="mobile_uploads/golf_shots"):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)  # Убедимся, что папка существует
        self.processed_videos = set(os.listdir(self.directory))  # Сохраняем существующие файлы как обработанные

    async def check_new_video(self):
        # Получаем текущий список файлов в папке
        current_files = set(os.listdir(self.directory))
        # Находим новые файлы
        new_files = current_files - self.processed_videos
        print('new_files', new_files)
        if new_files:
            print('in if new_files', new_files)
            for file_name in new_files:
                print('if for loop new_files', new_files, 'длинна', len(new_files))
                print(f"Найден новый файл: {file_name}")
                if len(new_files) == 1:
                    print('опаопа нашол')
                    await find_golf_ball(file_name)
            # Обновляем список обработанных файлов
            self.processed_videos = current_files

    async def check_folder(self):
        logger.info(f"Folder tracking: {self.directory}")
        while True:
            await self.check_new_video()
            await asyncio.sleep(1)


if __name__ == "__main__":
    check_folder = FolderWatcher()
    asyncio.run(check_folder.check_folder())
