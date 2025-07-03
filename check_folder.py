import os
import asyncio

from find_ball import find_golf_ball


class FolderWatcher:
    def __init__(self, directory):
        self.directory = directory
        # self.processed_files = set()
        self.processed_files = set(os.listdir(self.directory))  # Сохраняем существующие файлы как обработанные

        # Убедимся, что папка существует
        os.makedirs(self.directory, exist_ok=True)

    async def check_for_new_files(self):
        # Получаем текущий список файлов в папке
        current_files = set(os.listdir(self.directory))
        # Находим новые файлы
        new_files = current_files - self.processed_files
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
            self.processed_files = current_files

    async def check_folder(self):
        logger(f"Отслеживание папки: {self.directory}")
        while True:
            await self.check_new_files()
            await asyncio.sleep(1)


if __name__ == "__main__":
    check_folder = FolderWatcher()
    asyncio.run(check_folder.check_folder())
