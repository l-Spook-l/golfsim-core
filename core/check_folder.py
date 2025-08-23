import os
import asyncio

from core.find_ball import VideoProcessor
from core.logging_config import logger


class FolderWatcher:
    def __init__(self, directory="mobile_uploads/golf_shots"):
        self.directory = directory
        self.processed_videos = set()
        self.__running = False
        os.makedirs(self.directory, exist_ok=True)
        self._init_processed_files()

    def _init_processed_files(self):
        try:
            self.processed_videos = set(os.listdir(self.directory))
            logger.info(f"Initialized with {len(self.processed_videos)} processed files")
        except Exception as e:
            logger.error(f"Error initializing processed files: {e}")
            self.processed_videos = set()

    async def check_new_video(self):
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
        logger.info("Stopping folder watcher...")
        self.__running = False

        # if hasattr(find_golf_ball, 'close'):
        #     await find_golf_ball.close()

        logger.info("Folder watcher stopped gracefully")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
