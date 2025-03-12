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


async def check_folder_main():
    watcher = FolderWatcher("folder_test_all_open")
    print(f"Отслеживание папки: {watcher.directory}")

    # цикл проверки
    while True:
        await watcher.check_for_new_files()
        print('check_folder_main')
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(check_folder_main())
