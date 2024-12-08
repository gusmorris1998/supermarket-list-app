# Standard Libraries
from typing import List, Union
from typing_extensions import Annotated
import os, time, json, random, re

from pydantic import BaseModel, field_validator
from curl_cffi import requests
from dotenv import load_dotenv

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0'
}

load_dotenv()

class Category(BaseModel):
    NodeId: str
    Description: str
    UrlFriendlyName: str
    Children: List["Category"] = []

    class Config:
        # Allow recursive types (e.g., Children containing more Categories)
        arbitrary_types_allowed = True

def get_categories():
    url = f"{os.getenv("WOOLWORTHS_API")}/PiesCategoriesWithSpecials"

    resp = requests.get(url, proxy=os.getenv("PROXY_PORT_DC"))
    resp.raise_for_status()

    categories = [
        Category(**cat).model_dump_json() for cat in resp.json()["Categories"]
    ]

    with open(f"/{os.getenv("WDIR")}/scrape/storage/coles_cats.json", "w") as f:
        json.dump(categories, f, indent=4)


class AdditionalInformation(BaseModel):
    nutritionalinformation: str | None
    sapcategoryname: str | None
    PiesProductDepartmentsjson: str

class ProductDetails(BaseModel):
    # General Details
    Stockcode: int
    Price: float | None
    WasPrice: float
    CupPrice: float | None
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
    Name: str
    DisplayName: str

    @field_validator('Products', mode='before')
    @classmethod
    def validate_Products(cls, products):
        return [
            product for product in products
            if isinstance(product.get('Price'), (int, float))
        ]

    Products: List[ProductDetails]


class SearchResponse(BaseModel):
    TotalRecordCount: int

    @field_validator("Bundles", mode="before")
    def filter_invalid_bundles(cls, bundles):
        # Filter out Products with no valid ProductDetails
        return [
            bundle for bundle in bundles 
            if len(bundle.get("Products", [])) > 0
        ]

    Bundles: list[Product]


def new_session():
    session = requests.Session(impersonate="chrome", proxy=os.getenv("PROXY_PORT_DC"), headers=HEADERS, verify=False)
    return session

def search_api(session: requests.Session,
                catID: str,
                catURL: str,
                catOBJ: str,
                page_num: int) -> SearchResponse:

    url = f"{os.getenv("WOOLWORTHS_API")}/browse/category?categoryId={catID}&Url={catURL}&formatObject={catOBJ}&pageNumber={page_num}&pageSize=36"

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

def get_details(node, url):
    if re.search('SPECIALS', node['NodeId']):
        return (node['NodeId'],
                f"{url}/{node["UrlFriendlyName"]}",
                f'%7B"name":"{re.sub('&', '%26', node['Description'])}"%7D')
    
    return get_details(node["Children"][0], f"{url}/{node["UrlFriendlyName"]}")

def main():
    products = []
    with open(f"/{os.getenv("WDIR")}/scrape/storage/coles_cats.json") as f:
        json_data = json.load(f)[1:21]
        categories = [
            get_details(json.loads(node), '/shop/browse') for node in json_data
                        ]
    session = new_session()
    
    for catID, catURL, catOBJ in categories:
        page_num = 1
        while True:
            time.sleep(random.randint(1,3))

            search = search_api(session, catID, catURL, catOBJ, page_num)

            if search.Bundles:
                print(search.Bundles[0].Name)
            else:
                print("Category End")
                break
            
            products = products + [p.model_dump_json()  for p in search.Bundles]

            page_num += 1

    with open(f"/{os.getenv("WDIR")}/scrape/storage/coles_products.json", "w") as f:
        json.dump(products, f, indent=4)

if __name__ ==  "__main__":
    main()