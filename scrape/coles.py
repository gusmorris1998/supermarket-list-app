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

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0'
}

load_dotenv()

class Product(BaseModel):
    # General Details
    _type: Literal["PRODUCT"]
    id: int
    name: str
    size = str

    # Dicts
    pricing: dict
    merchandiseHeir: dict

class SearchResponse(BaseModel):
    noOfResults: int
    pageSize: int
    start: int
    results: list[Product | None]

    @validator('results', pre=True, each_item=True)
    def filter_non_product(cls, v):
        if v.get("_type") == "PRODUCT":
            return v  # Keep entry if it's a "PRODUCT"
        return None  # Discard entry
    
    def __init__(self, **data):
        super().__init__(**data)
        # Filter out None values from results
        self.results = [result for result in self.results if result is not None]

def new_session():
    session = requests.Session(impersonate="chrome", proxy=os.getenv("PROXY"), headers=HEADERS, verify=False)
    return session

def search_api(session: requests.Session, page_num: int) -> SearchResponse: 
    url = f"https://www.coles.com.au/_next/data/20241113.01_v4.30.0/en/on-special.json?page={page_num}"

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

def main():

    page_num=1
    session = new_session()
    
    search = search_api(session, page_num)
    products = [p.json() for p in search.results]

    no_pages = search.noOfResults // (search.pageSize + 1)

    while page_num < no_pages:
        page_num += 1
        time.sleep(random.randint(1,3))

        search = search_api(session, page_num)
        print(search.start)

        products = products + [p.json() for p in search.results]

    with open("../storage/data.json", "w") as f:
        json.dump(products, f, indent=4)

if __name__ ==  "__main__":
    main()



        



        



