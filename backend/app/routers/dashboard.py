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

@router.get("/get_total_employer")
async def get_total_employer(request: Request):
    """获取雇主总数"""
    return Dashboard().get_total_employer()

@router.get("/get_employer_by_limit")
async def get_employer_by_limit(request: Request, page, num):
    """获取区间雇主列表"""
    return Dashboard().get_employer_by_limit(page, num)

@router.get("/get_employer")
async def get_employer(request: Request, employer):
    """检索雇主是否存在"""
    return Dashboard().get_employer(employer)

@router.get("/get_total_by_employer")
async def get_total_by_employer(request: Request, employer):
    """根据雇主名称获取招聘数量"""
    return Dashboard().get_total_by_employer(employer)

@router.get("/get_employer_data_by_limit")
async def get_employer_data_by_limit(request: Request, employer, page, num):
    """获取雇主的区间数据"""
    return Dashboard().get_employer_data_by_limit(employer, page, num)

@router.get("/get_all_province")
async def get_all_province(request: Request):
    """获取所有省份名称"""
    return Dashboard().get_all_province()

@router.get("/get_city_by_province")
async def get_city_by_province(request: Request, province):
    """获取省份下属市县名称"""
    return Dashboard().get_city_by_province(province)

@router.get("/get_map_by_country", response_class=HTMLResponse)
async def get_map_by_country(request: Request, country):
    """获取国级展示图"""
    return Dashboard().get_map_by_country(country)

@router.get("/get_map_by_province", response_class=HTMLResponse)
async def get_map_by_country(request: Request, province):
    """获取省级展示图"""
    return Dashboard().get_map_by_province(province)
