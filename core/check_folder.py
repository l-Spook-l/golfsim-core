import os
import asyncio

from core.find_ball import VideoProcessor
from core.logging_config import logger


class FolderWatcher:
    """
    Class for monitoring a folder and processing new video files.

    FolderWatcher tracks the appearance of new videos in the specified directory
    and starts asynchronous processing via VideoProcessor.
    It is used for automatic processing of uploaded files (golf shots).
    """

    def __init__(self, directory: str = "mobile_uploads/golf_shots"):
        """
        Args:
            directory (str): Folder to monitor.
        """
        self.directory = directory
        self.processed_videos = set()
        self.__running = False
        os.makedirs(self.directory, exist_ok=True)
        self._init_processed_files()

    def _init_processed_files(self):
        """
        Loads the list of already existing files in the folder to avoid reprocessing.
        """
        try:
            self.processed_videos = set(os.listdir(self.directory))
            logger.info(f"Initialized with {len(self.processed_videos)} processed files")

        except Exception as e:
            logger.error(f"Error initializing processed files: {e}")
            self.processed_videos = set()

    async def check_new_video(self):
        """
        Checks for new files in the folder and starts their processing.

        - Filters by extensions: .mp4, .avi, .mov.
        - For each new file, calls VideoProcessor(file_name).run().
        """
        try:
            current_files = set(os.listdir(self.directory))
            new_files = current_files - self.processed_videos
            logger.info(f'new_files - {new_files}')

            if new_files:
                logger.info(f"Found {len(new_files)} new files")
                for file_name in new_files:
                    if file_name.lower().endswith(('.mp4', '.avi', '.mov')):
                        logger.info(f"Processing new video: {file_name}")
                        await VideoProcessor(file_name).run()
                self.processed_videos.update(new_files)

        except Exception as e:
            logger.error(f"Error checking new videos: {e}")

    async def check_folder(self):
        """
        Starts the folder watching loop.

        Asynchronous method that checks for new files every 1 second
        and processes them until close() is called.

        Raises:
            asyncio.CancelledError: When stopped via task cancellation.
        """
        self.__running = True
        logger.info(f"Starting folder watcher for: {self.directory}")

        while self.__running:
            try:
                await self.check_new_video()
            except asyncio.CancelledError:
                logger.info("Folder watcher received cancellation")
                break
            except Exception as e:
                logger.error(f"Unexpected error in folder watcher: {e}")

            await asyncio.sleep(1)

        logger.info("Folder watcher stopped")

    async def close(self):
        """
        Stops folder monitoring and shuts down asynchronously.
        """
        logger.info("Stopping folder watcher...")
        self.__running = False
        logger.info("Folder watcher stopped gracefully")

    async def __aenter__(self):
        """
        Supports asynchronous context manager.

        Returns:
            FolderWatcher: An instance of FolderWatcher.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Shuts down the watcher when exiting the context manager.
        """
        await self.close()
