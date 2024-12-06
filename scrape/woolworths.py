# Standard Libraries
from typing import Literal
import os, time, json, random

from pydantic import BaseModel, field_validator
from curl_cffi import requests
from dotenv import load_dotenv

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0'
}

CATEGORIES = [
    ('1-E5BEE36E_SPECIALS', '/shop/browse/fruit-veg/fruit-veg-specials', '%7B%22name%22:%22Fruit%20%26%20Veg%20Specials%22%7D')
]

load_dotenv()

# --- Model Data ---

class AdditionalInformation(BaseModel):
    nutritionalinformation: dict
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
    session = requests.Session(impersonate="chrome", proxy=os.getenv("PROXY_PORT_DC"), headers=HEADERS, verify=False)
    return session

def search_api(session: requests.Session,
                catID: str,
                catURL: str,
                catOBJ: str,
                page_num: int) -> SearchResponse:

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

    search = SearchResponse(**resp.json())
    return search

def main():
    products = []

    page_num=1
    session = new_session()
    
    for catID, catURL, catOBJ in CATEGORIES:
        page_end = False
        while not page_end:
            page_num += 1
            time.sleep(random.randint(1,3))

            search = search_api(session, catID, catURL, catOBJ)
            print(search.Bundles[0].Name if search.Bundles else "Category End")
            
            products = products + [p.json for p in search.Bundles]

    # This hasn't worked previously, likely needs changing
    with open("../storage/data.json", "w") as f:
        json.dump(products, f, indent=4)