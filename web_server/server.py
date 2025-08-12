import asyncio
import os

import uvicorn
import aiofiles
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from web_server.find_local_ip import get_local_ip as local_ip
from data_base.config_db import async_session_maker
from data_base.repositories.hsv_setting import HSVSettingRepository
from data_base.schemas import HSVSettingSchema
from logging_config import logger


class APIServer:
    def __init__(self):
        self.server = None
        self.app = FastAPI(lifespan=self.lifespan)
        self.BASE_UPLOAD_DIR = "mobile_uploads"
        self.state = {"status": False}
        self._setup_routes()
        self._setup_middleware()

    def _setup_routes(self):
        @self.app.post("/upload")
        async def upload_file(file: UploadFile = File(...)):
            file_type = file.content_type.split("/")[0]
            subdir = "images" if file_type == "image" else "golf_shots"
            upload_dir = os.path.join(self.BASE_UPLOAD_DIR, subdir)
            file_path = os.path.join(upload_dir, file.filename)

            try:
                async with aiofiles.open(file_path, "wb") as buffer:
                    while chunk := await file.read(1024 * 1024):  # Читаем по 1 МБ
                        await buffer.write(chunk)
                return {"filename": file.filename}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

        @self.app.post("/putting")
        async def putting(angle: int):
            return {"angle": angle}

        @self.app.get("/status")
        async def get_status():
            return {"status": self.state["status"]}

        @self.app.post("/update-status")
        async def update_status(new_state: dict):
            self.state["status"] = new_state.get("status", self.state["status"])
            return {"status": self.state["status"]}

        @self.app.get("/local-ip")
        async def get_local_ip():
            ip = local_ip()
            return {"local_ip": ip}

        @self.app.get("/get-hsv")
        async def get_hsv() -> dict:
            async with async_session_maker() as session:
                repo = HSVSettingRepository(session)
                data = await repo.get_active_hsv_set()
                logger.info(f"Data active_hsv - {data}")
            hsv_schema = HSVSettingSchema.model_validate(data)
            return {"hsv_vals": hsv_schema.model_dump()}

    def _setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        # Startup logic
        logger.info("Starting server...")
        yield
        # Shutdown logic
        logger.info("Stopping server...")

    async def start(self):
        config = uvicorn.Config(
            self.app,
            host="192.168.50.107",
            port=7878,
            lifespan="on"
        )
        self.server = uvicorn.Server(config)
        await self.server.serve()

    async def stop(self):
        if self.server:
            self.server.should_exit = True
            try:
                await self.server.shutdown()
            except Exception as e:
                logger.error(f"Error stopping server: {e}")


if __name__ == "__main__":
    server = APIServer()
    asyncio.run(server.start())
