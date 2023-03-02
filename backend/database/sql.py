# -*- coding:utf-8 -*-
BASE_SQL = """SELECT * FROM sme_cdc_data;"""
FUZZY_SEARCH_TARGET_SCHOOL = """SELECT distinct(offer_school) FROM sme_cdc_data;"""
FUZZY_SEARCH_TARGET_MAJOR = """SELECT distinct(offer_major) FROM sme_cdc_data;"""
GET_PWD_BY_USER = """SELECT password FROM sme_cdc_user WHERE username='{username}' LIMIT 1;"""
GET_TOTAL_EMPLOYER = """SELECT COUNT(DISTINCT(employer)) FROM dashboard_data;"""
GET_EMPLOYER_BY_LIMIT = """SELECT DISTINCT(employer) FROM dashboard_data LIMIT {limit} OFFSET {offset};"""
GET_EMPLOYER = """SELECT DISTINCT(employer) FROM dashboard_data WHERE employer='{employer}';"""
GET_EMPLOYER_DATA_BY_LIMIT = """SELECT * FROM dashboard_data WHERE employer='{employer}' LIMIT {limit} OFFSET {offset};"""
GET_TOTAL_BY_EMPLOYER = """SELECT COUNT(*) FROM dashboard_data WHERE employer='{employer}';"""
GET_ALL_PROVINCE = """SELECT DISTINCT(province) FROM province_city_map;"""
GET_ALL_CITY = """SELECT DISTINCT(city) FROM province_city_map WHERE province='{province}';"""
GET_CITY_BY_PROVINCE = """SELECT DISTINCT(city) FROM province_city_map WHERE province='{province}';"""
