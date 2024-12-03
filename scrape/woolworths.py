# Standard Libraries
from typing import Literal
import os, time, json, random

from pydantic import BaseModel, validator
from curl_cffi import requests
from dotenv import load_dotenv

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0'
}

CATEGORIES = {
    '1-E5BEE36E_SPECIALS': ('/shop/browse/fruit-veg/fruit-veg-specials', '%7B%22name%22:%22Fruit%20%26%20Veg%20Specials%22%7D')
}

load_dotenv()

# --- Model Data ---

class AdditionalInformation(BaseModel):
    nutritionalinformation: Json
    sapcategoryname: str
    PiesProductDepartmentsjson: str

class ProductDetails(BaseModel):
    # General Details
    Stockcode: int
    Price: float
    WasPrice: float
    CupPrice: int | None
    CupMeasure: str | None
    IsNew: bool
    IsAvailable: bool
    IsForCollection: bool
    IsForDelivery: bool
    Unit: str
    Brand: str | None

    MediumImageFile: str
    AdditionalAttributes: AdditionalInformation

class Product(BaseModel):
    Products: list[ProductDetails]
    Name: str
    DisplayName: str


class SearchResponse(BaseModel):
    TotalRecordCount: int
    Bundles: list[Product]

def new_session():
    session = requests.Session(impersonate="chrome", proxy=os.getenv("PROXY"), headers=HEADERS, verify=False)
    return session

def search_api(session: requests.Session, page_num: int) -> SearchResponse:

    url = f"https://www.woolworths.com.au/apis/ui/browse/category?
            categoryId={catID}&
            Url={catURL}&
            formatObject={catOBJ}&
            pageNumber={page_num}"

    resp = session.get(url)

    i = 1
    while i <= 3 and not resp.ok:
        try:
            resp.raise_for_status()
        except:
            time.sleep(i*2)
            resp = session.get(url)

    resp.raise_for_status()

    search = SearchResponse(**resp.json()["pageProps"]["searchResults"])
    return search

