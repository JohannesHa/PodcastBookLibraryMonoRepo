from paapi5_python_sdk.rest import ApiException
from paapi5_python_sdk.models.search_items_resource import SearchItemsResource
from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.api.default_api import DefaultApi
from typing import List, Dict
from ...main import id_nlp
import os
from dotenv import load_dotenv

load_dotenv()

ENTITY_LABEL = "BOOK_TITLE"


def get_book_titles(sentences) -> List[str]:
    # doc = id_nlp(sentences)
    # return [(ent.text, ent.label_) for ent in doc.ents]
    book_titles = []

    for doc in id_nlp.pipe(sentences):
        for ent in doc.ents:
            if ent.label_ == ENTITY_LABEL:
                if ent.text not in book_titles:
                    book_titles.append(ent.text)
                print("Document text: ", doc.text)
                print("Book Title: ", ent.text)
    return book_titles


def search_amazon_api_for_book(book_title):
    access_key = os.getenv('AMAZON_API_ACCESS_KEY')
    secret_key = os.getenv('AMAZON_API_SECRET_KEY')
    partner_tag = os.getenv('AMAZON_API_PARTNER_TAG')

    host = "webservices.amazon.com"
    region = "us-east-1"

    default_api = DefaultApi(
        access_key=access_key, secret_key=secret_key, host=host, region=region
    )

    # Specify keywords
    keywords = book_title
    search_index = "Books"

    # Specify item count to be returned in search result
    item_count = 1

    # Choose resources you want from SearchItemsResource enum
    # For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter
    search_items_resource = [
        SearchItemsResource.ITEMINFO_BYLINEINFO,
        SearchItemsResource.ITEMINFO_TITLE,
        SearchItemsResource.ITEMINFO_CONTENTINFO,
        SearchItemsResource.OFFERS_LISTINGS_PRICE,
        SearchItemsResource.IMAGES_PRIMARY_LARGE,
    ]

    # Forming request
    try:
        search_items_request = SearchItemsRequest(
            partner_tag=partner_tag,
            partner_type=PartnerType.ASSOCIATES,
            keywords=keywords,
            search_index=search_index,
            item_count=item_count,
            resources=search_items_resource,
        )
    except ValueError as exception:
        print("Error in forming SearchItemsRequest: ", exception)
        return

    try:
        # Sending request
        response = default_api.search_items(search_items_request)

        print("API called Successfully")
        print("Complete Response:", response)

        # Parse response
        if response.search_result is not None:
            print("Printing first item information in SearchResult:")
            item_0 = response.search_result.items[0]
            if item_0 is not None:
                if item_0.asin is not None:
                    print("ASIN: ", item_0.asin)
                if item_0.detail_page_url is not None:
                    print("DetailPageURL: ", item_0.detail_page_url)
                if (
                    item_0.item_info is not None
                    and item_0.item_info.title is not None
                    and item_0.item_info.title.display_value is not None
                ):
                    print("Title: ", item_0.item_info.title.display_value)
                if (
                    item_0.offers is not None
                    and item_0.offers.listings is not None
                    and item_0.offers.listings[0].price is not None
                    and item_0.offers.listings[0].price.display_amount is not None
                ):
                    print(
                        "Buying Price: ", item_0.offers.listings[0].price.display_amount
                    )

            return item_0
        if response.errors is not None:
            print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
            print("Error code", response.errors[0].code)
            print("Error message", response.errors[0].message)

    except ApiException as exception:
        print("Error calling PA-API 5.0!")
        print("Status code:", exception.status)
        print("Errors :", exception.body)
        print("Request ID:", exception.headers["x-amzn-RequestId"])

    except TypeError as exception:
        print("TypeError :", exception)

    except ValueError as exception:
        print("ValueError :", exception)

    except Exception as exception:
        print("Exception :", exception)
