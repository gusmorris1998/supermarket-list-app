# Standard Libraries
from typing import Literal
import os, time, json, random

from pydantic import BaseModel, validator
from curl_cffi import requests
from dotenv import load_dotenv

# PROXIES = {
#     'http': '127.0.0.1:24000',
#     'https': '127.0.0.1:24000'
# }

PROXY = '127.0.0.1:24000'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0'
}

load_dotenv()