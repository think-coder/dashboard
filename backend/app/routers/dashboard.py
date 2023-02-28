# -*- coding:utf-8 -*-
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request

from app.models.dashboard import Dashboard

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={
        404: {"description": "Not found"}
    },
)

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return Dashboard().get_dashboard()
