import logging

logger = logging.getLogger("app")
# Set the logging level
# If .setLevel(logging.WARNING) is set, INFO and DEBUG will not be displayed.
logger.setLevel(logging.DEBUG)

# Message format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Output to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Output to file (if needed)
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
