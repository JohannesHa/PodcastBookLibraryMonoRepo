from ..apis.nlp.booktitles import get_book_titles, search_amazon_api_for_book
from ..apis.nlp.preprocessing import preprocess_transcript
from typing import Optional, List
from fastapi import APIRouter
from pydantic import BaseModel


class NerQuery(BaseModel):
    s3Url: str


router = APIRouter(
    prefix='/nlp/id',
    tags=['nlp'],
    responses={
        404: {'description': 'Not Found'}
    }
)


# send a transcript and get all book recommendations in JSON format
@router.post('/book-recommendations')
async def api_ner(query: NerQuery):

    s3_transcript_url = query.s3Url

    print("START PROCESSING OF TRANSCRIPT")
    sentences_with_book_context = preprocess_transcript(s3_transcript_url)

    print("FINISHED PREPROCESSING OF TRANSCRIPT")
    print("sentences_with_book_context", sentences_with_book_context)

    recommended_book_titles = get_book_titles(sentences_with_book_context)

    print("FINISHED EXTRACTING BOOK TITLES")
    print("recommended_book_titles ", recommended_book_titles)

    results = []

    for book_title in recommended_book_titles:
        book_api_result = search_amazon_api_for_book(book_title)
        if book_api_result is not None:

            book_id_result = book_api_result.asin
            book_title_result = book_api_result.item_info.title.display_value
            book_contributors_result = book_api_result.item_info.by_line_info.contributors
            book_authors = [
                contributor.name for contributor in book_contributors_result if contributor.role == 'Author']
            book_url_result = book_api_result.detail_page_url
            book_img_result = book_api_result.images.primary.large.url

            book_recommendation = {
                "id": book_id_result,
                "title": book_title_result,
                "authors": book_authors,
                "amazonUrl": book_url_result,
                "imageUrl": book_img_result,
                "apiResult": book_api_result
            }

            results.append(book_recommendation)

    print("FINISHED AMAZON API CALL")
    print("Results: ", results)

    return results
