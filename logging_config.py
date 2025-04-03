import logging

logger = logging.getLogger("app")
# Устанавливаем уровень логирования
logger.setLevel(logging.DEBUG)  # Если стоит .setLevel(logging.WARNING), то INFO и DEBUG не будут отображаться.

# Формат сообщений
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Вывод в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Вывод в файл (если нужно)
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


