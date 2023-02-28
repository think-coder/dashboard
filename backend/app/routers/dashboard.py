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

@router.get("/get_total_employer")
async def get_total_employer(request: Request):
    return Dashboard().get_total_employer()

@router.get("/get_employer_by_limit")
async def get_employer_by_limit(request: Request, page, num):
    return Dashboard().get_employer_by_limit(page, num)

@router.get("/get_employer")
async def get_employer(request: Request, employer):
    return Dashboard().get_employer(employer)

@router.get("/get_total_by_employer")
async def get_total_by_employer(request: Request, employer):
    return Dashboard().get_total_by_employer(employer)

@router.get("/get_employer_data_by_limit")
async def get_employer_data_by_limit(request: Request, employer, page, num):
    return Dashboard().get_employer_data_by_limit(employer, page, num)
