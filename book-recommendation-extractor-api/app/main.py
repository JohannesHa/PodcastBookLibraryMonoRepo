import time 
import random
import string
import logging
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from pathlib import Path
import spacy

logging.info("loading custom spacy nlp model")
model_dir = Path('nlp_models/transformer-model-best-07-04-2021')
print(model_dir)
id_nlp = spacy.load(model_dir)
logging.info("done loading spacy nlp model")

app = FastAPI()

# set logger middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    rid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={rid} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)

    logger.info(f"rid={rid} completed in = {formatted_process_time}ms status_code={response.status_code}")
    return response

# set cors 
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

from .routes import nlp

app.include_router(nlp.router)

# default root path 
@app.get('/')
async def root():
    return {
        'message':  'SpaCy x FastAPI x Book Recommendation Extractor'
    }