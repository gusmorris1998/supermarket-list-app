# Standard Libraries
from typing import Literal, List, Any, Optional
import os, time, json, random

from pydantic import BaseModel, field_validator
from curl_cffi import requests
from dotenv import load_dotenv

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0'
}

load_dotenv()

class Category(BaseModel):
    id: str
    level: int
    name: str
    originalName: str
    catalogGroupView: List["Category"] = []
    productCount: int

    class Config:
        # Allow recursive types (e.g., Children containing more Categories)
        arbitrary_types_allowed = True

def get_categories():
    json_data = {
    'query': '\n    query GetProductCategories($storeId: BrandedId!, $withCampaignLinks: Boolean!, $campaignCount: Int) {\n  productCategories(\n    storeId: $storeId\n    withCampaignLinks: $withCampaignLinks\n    campaignCount: $campaignCount\n  ) {\n    ...productCategoriesFields\n  }\n}\n    \n    fragment productCategoriesFields on ProductCategories {\n  excludedCategoryIds\n  catalogGroupView {\n    ...catalogGroupFields\n    catalogGroupView {\n      ...catalogGroupFields\n      catalogGroupView {\n        ...catalogGroupFields\n      }\n    }\n  }\n}\n    \n    fragment catalogGroupFields on ProductCategory {\n  id\n  level\n  name\n  originalName\n  productCount\n  seoToken\n  type\n}\n    ',
    'variables': {
        'storeId': 'COL:512',
        'withCampaignLinks': False,
    },
    'operationName': 'GetProductCategories',
}
    cookies = {
        'visid_incap_2800108': 'xCHbqHKvTs6XYjJu2ki6D7U4VGcAAAAAQUIPAAAAAADFQulN3t02f+q2uiOygfxC',
        'incap_ses_361_2800108': 's6Xvd9BWgUZqHDJHx4cCBbU4VGcAAAAAH0+28AHrFtCoWF91fnJ+UA==',
        'AMCVS_0B3D037254C7DE490A4C98A6%40AdobeOrg': '1',
        'AMCV_0B3D037254C7DE490A4C98A6%40AdobeOrg': '179643557%7CMCIDTS%7C20065%7CMCMID%7C11519788548200838052708678877733750465%7CMCAID%7CNONE%7CMCOPTOUT-1733579991s%7CNONE%7CvVersion%7C5.5.0',
        'nlbi_2800108_2147483392': '4xbpfg2BLwtUEHHUjQyMFgAAAACDdUQhnRORD7+Odf/W0WRn',
        'reese84': '3:4nXhj8drlacAuckrgXtqHA==:ggEw/rViZTny6JMt67o6ihaDGeq/FhIuNRi044dMIG6LPtYoPLTOrebt07Z72VHf1PwwXi8Isgi0/Y41WVKMvJ56WmYq6cqD8OCz1fsdNDZD5lA24uNjOKlPNQyEsEXXqiMoYljtTEp8DzSHilv41Vxtlcxv4oFcpeUuJiDM0UgSSh1bWCFykq+9Pjok1zBA0tnG/Ov6BtcV6TzR+oxNtpk+T8IoGGWQXFM60BCk8hMe8v3mrII3DnY4nrXl+exdcCbVeISH/myYcMJ9JOSAgdzr5EDDPNZajnn7hbl4F/eftucGd7Y3UBxbgmNdeoCjPhPKHfwswIklPV4eYVsfgBzPuQQtnbwX/IJjauKplIOXNPjMeosU2yVvQDwb///DUuhKy5MvkyKe6ut6s8XrDU626VyqTlApVcCYuFMGrlVo19KFordEucmQpkvc7SoZXuKQ2WZjTsmQ2uSPMsD5Sw==:exZeCT8KdU2fvUd0fp1O8mY1qkA9TR6nbij3ku5sFUk=',
        'ld_user': 'c901501c-be39-4fdc-a426-8aaab5cdc444',
        'sessionId': '8a83b5c0-efe3-4376-a968-28032fa25f7f',
        'visitorId': '9ee79307-bda0-4b2a-85fe-cf0de56311fd',
        'nlbi_2800108_3037207': '5P5PX79tf1s8QDwqjQyMFgAAAAAVzzwEhA7ZWsrQVNTPTP+m',
        'analyticsIsLoggedIn': 'false',
        'at_check': 'true',
        'mbox': 'session#70822cdd1da14a5bb45ed07985ac0360#1733574657|PC#70822cdd1da14a5bb45ed07985ac0360.36_0#1796817597',
        'fulfillmentStoreId': '0512',
        'shopping-method': 'clickAndCollect',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        # 'cookie': 'visid_incap_2800108=xCHbqHKvTs6XYjJu2ki6D7U4VGcAAAAAQUIPAAAAAADFQulN3t02f+q2uiOygfxC; incap_ses_361_2800108=s6Xvd9BWgUZqHDJHx4cCBbU4VGcAAAAAH0+28AHrFtCoWF91fnJ+UA==; AMCVS_0B3D037254C7DE490A4C98A6%40AdobeOrg=1; AMCV_0B3D037254C7DE490A4C98A6%40AdobeOrg=179643557%7CMCIDTS%7C20065%7CMCMID%7C11519788548200838052708678877733750465%7CMCAID%7CNONE%7CMCOPTOUT-1733579991s%7CNONE%7CvVersion%7C5.5.0; nlbi_2800108_2147483392=4xbpfg2BLwtUEHHUjQyMFgAAAACDdUQhnRORD7+Odf/W0WRn; reese84=3:4nXhj8drlacAuckrgXtqHA==:ggEw/rViZTny6JMt67o6ihaDGeq/FhIuNRi044dMIG6LPtYoPLTOrebt07Z72VHf1PwwXi8Isgi0/Y41WVKMvJ56WmYq6cqD8OCz1fsdNDZD5lA24uNjOKlPNQyEsEXXqiMoYljtTEp8DzSHilv41Vxtlcxv4oFcpeUuJiDM0UgSSh1bWCFykq+9Pjok1zBA0tnG/Ov6BtcV6TzR+oxNtpk+T8IoGGWQXFM60BCk8hMe8v3mrII3DnY4nrXl+exdcCbVeISH/myYcMJ9JOSAgdzr5EDDPNZajnn7hbl4F/eftucGd7Y3UBxbgmNdeoCjPhPKHfwswIklPV4eYVsfgBzPuQQtnbwX/IJjauKplIOXNPjMeosU2yVvQDwb///DUuhKy5MvkyKe6ut6s8XrDU626VyqTlApVcCYuFMGrlVo19KFordEucmQpkvc7SoZXuKQ2WZjTsmQ2uSPMsD5Sw==:exZeCT8KdU2fvUd0fp1O8mY1qkA9TR6nbij3ku5sFUk=; ld_user=c901501c-be39-4fdc-a426-8aaab5cdc444; sessionId=8a83b5c0-efe3-4376-a968-28032fa25f7f; visitorId=9ee79307-bda0-4b2a-85fe-cf0de56311fd; nlbi_2800108_3037207=5P5PX79tf1s8QDwqjQyMFgAAAAAVzzwEhA7ZWsrQVNTPTP+m; analyticsIsLoggedIn=false; at_check=true; mbox=session#70822cdd1da14a5bb45ed07985ac0360#1733574657|PC#70822cdd1da14a5bb45ed07985ac0360.36_0#1796817597; fulfillmentStoreId=0512; shopping-method=clickAndCollect',
        'cusp-correlation-id': 'e4263d7c-4d36-4492-a897-5a6b0cbcf62d',
        'cusp-session-id': '8a83b5c0-efe3-4376-a968-28032fa25f7f',
        'cusp-user-id': '',
        'cusp-visitor-id': '9ee79307-bda0-4b2a-85fe-cf0de56311fd',
        'dsch-channel': 'coles.online.1site.desktop',
        'ocp-apim-subscription-key': 'eae83861d1cd4de6bb9cd8a2cd6f041e',
        'origin': 'https://www.coles.com.au',
        'priority': 'u=1, i',
        'referer': 'https://www.coles.com.au/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    response = requests.post(f'{os.getenv('COLES_API')}/graphql',
                            headers=headers,
                            cookies=cookies,
                            json=json_data)
                            # proxy=os.getenvb('PROXY_PORT_DC'))

    categories = [
        Category(**cat).model_dump_json() for cat in response.json()['data']['productCategories']['catalogGroupView']
    ]

    with open(f"/{os.getenv("WDIR")}/scrape/storage/coles_cats.json", "w") as f:
        json.dump(categories, f, indent=4)


class Product(BaseModel):
    # General Details
    _type: Literal["PRODUCT"]
    id: int
    name: str
    brand: str | None
    size: str

    # Dicts
    pricing: dict
    merchandiseHeir: dict
    onlineHeirs: Optional[List[dict]] = None  # Allow missing `onlineHeirs`

class SearchResponse(BaseModel):
    noOfResults: int
    pageSize: int
    start: int
    results: list[Product | None]

    @field_validator("results", mode="before")
    def filter_non_product(cls, results: Any) -> Any:
        # Ensure only valid Product objects with "_type" == "PRODUCT" and "pricing" are kept
        filtered_results = []
        for item in results:
            if not isinstance(item, dict):  # Discard non-dict entries early
                continue
            if item.get("_type") == "PRODUCT" and item.get("pricing") is not None:
                filtered_results.append(item)
        return filtered_results

def new_session():
    session = requests.Session(impersonate="chrome",
                                proxy=os.getenv("PROXY"),
                                headers=HEADERS,
                                verify=False)
    return session

def search_api(session: requests.Session, page_num: int) -> SearchResponse: 
    url = f"{os.getenv("COLES_DATA_API")}/en/on-special.json?page={page_num}"

    resp = session.get(url)
    for i in range(1, 4):
        if resp.ok:
            break
        time.sleep(i * 2)
        resp = session.get(url)

    resp.raise_for_status()

    search = SearchResponse(**resp.json()["pageProps"]["searchResults"])
    return search

def main():

    page_num=1
    session = new_session()
    
    search = search_api(session, page_num)
    products = [p.model_dump_json() for p in search.results]

    no_pages = search.noOfResults // (search.pageSize + 1)

    while page_num < no_pages:
        page_num += 1
        time.sleep(random.randint(1,3))

        search = search_api(session, page_num)
        print(search.start)

        products = products + [p.model_dump_json() for p in search.results]

        with open(f"/{os.getenv("WDIR")}/scrape/storage/coles_products.json", "w") as f:
            json.dump(products, f, indent=4) 

if __name__ ==  "__main__":
    main()



        



        



