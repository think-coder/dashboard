# -*- coding:utf-8 -*-
BASE_SQL = """SELECT * FROM sme_cdc_data"""
FUZZY_SEARCH_TARGET_SCHOOL = """SELECT distinct(offer_school) FROM sme_cdc_data"""
FUZZY_SEARCH_TARGET_MAJOR = """SELECT distinct(offer_major) FROM sme_cdc_data"""
GET_PWD_BY_USER = """SELECT password FROM sme_cdc_user WHERE username='{username}' LIMIT 1"""
