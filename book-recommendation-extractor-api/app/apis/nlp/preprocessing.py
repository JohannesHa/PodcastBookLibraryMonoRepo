
import spacy
from spacy.matcher import PhraseMatcher
import requests
from ...main import id_nlp

phrase_matcher = PhraseMatcher(id_nlp.vocab)
phrases = ['book', 'books', 'i read', 'everyone should read',
           'you should read', 'he wrote a novel']


def preprocess_transcript(s3_transcript_url):
    # try to preprocess the podcast episode first and only keep sentences with book related words
    patterns = [id_nlp(text) for text in phrases]
    phrase_matcher.add('BOOK_NAME', None, *patterns)

    sentences_with_book_context = []

    transcript = requests.get(s3_transcript_url).text

    for sent in transcript.splitlines():
        for match_id, start, end in phrase_matcher(id_nlp(sent)):
            if id_nlp.vocab.strings[match_id] in ["BOOK_NAME"]:
                print(sent)
                sentences_with_book_context.append(sent)
                break
    return sentences_with_book_context
