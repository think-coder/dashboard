# -*- coding:utf-8 -*-
import uvicorn
from app.routers import dashboard
from fastapi  import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

templates = Jinja2Templates(directory="./templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")

if __name__ == "__main__":
    app.include_router(dashboard.router)
    uvicorn.run(app, host="0.0.0.0", port=8000)
