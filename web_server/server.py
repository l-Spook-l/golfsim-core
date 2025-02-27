import os

import uvicorn
import aiofiles
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .find_local_ip import get_local_ip as local_ip


app = FastAPI()

# Путь к общей папке на компьютере
UPLOAD_DIRECTORY = "folder_test_all_open"

# Убедитесь, что папка существует
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@app.get("/")
async def hello():
    return "Hello world, i'm working!"


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):  # Читаем по 1 МБ
                await buffer.write(chunk)
        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@app.post("/putting/")
async def putting(angle: int):
    return {"angle": angle}


# Разрешаем CORS для приложения
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Замените на домен вашего приложения
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Хранилище состояния
state = {"status": False}


@app.get("/status")
async def get_status():
    return {"status": state["status"]}


@app.post("/update-status")
async def update_status(new_state: dict):
    state["status"] = new_state.get("status", state["status"])
    return {"status": state["status"]}


@app.get("/local-ip")
async def get_local_ip():
    ip = local_ip()
    return {"local_ip": ip}


hsv_state = {"hsv_vals": {}}


@app.get("/get-hsv")
async def get_hsv():
    return {"hsv_vals": hsv_state}


@app.post("/update-hsv")
async def update_status(hsv_vals: dict):
    hsv_state["hsv_vals"] = hsv_vals  # Сохраняем данные в памяти
    print("Полученные HSV значения:", hsv_vals)
    return {"status": "ok", "received": hsv_vals}


# if __name__ == "__main__":
async def start_server():
    config = uvicorn.Config(
        "web_server.server:app",
        host="192.168.50.107",  # Фиксированный IP
        port=8000,  # Порт, на котором будет запущен сервер
        reload=True  # Автоматическая перезагрузка при изменении кода (опционально)
    )
    server = uvicorn.Server(config)
    await server.serve()
