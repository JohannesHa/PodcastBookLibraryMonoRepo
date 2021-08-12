from yt_scraper.scraper import scrape_from_yt
from hs_scraper.scraper import scrape_from_hs
import os
import logging
from time import sleep
from airtable import Airtable
from dotenv import load_dotenv

from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()

logging.getLogger().setLevel(logging.INFO)

AIRTABLE_BASE_KEY = os.getenv('AIRTABLE_BASE_KEY')
AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')

# Connects to Airtable
airtable = Airtable(AIRTABLE_BASE_KEY, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)
page = airtable.get_all()

sleep(2)
if not os.path.exists('./transcriptsNEW'):
    os.makedirs('./transcriptsNEW')

i = 0

for record in page:
    record_fields = record["fields"]
    if record_fields["Podcast Name"]:
        name_raw = record_fields["Podcast Name"]
        source_type_raw = record_fields["Where to find? (Youtube or HappyScribe until now)"]
        uri_raw = record_fields["URI (Youtube Playlist ID or HappyScribe URI)"]

        name = name_raw.lower().replace(" ", "_")
        source_type = "hs"
        if "youtube" in source_type_raw.lower():
            source_type = "yt"

        uri = "".join(uri_raw.split())

        # Init neccessary folder names & path
        folder_name = str(i) + "_" + name
        folder_path = "./transcriptsNEW/{}".format(folder_name)
        folder_path_relative = "transcriptsNEW/{}/".format(folder_name)

        i += 1

        logging.info("Start podcast scraping for {}".format(name))
        logging.info("----------------------------------")

        if not os.path.exists(folder_path):
            try:
                os.mkdir(folder_path)
            except Exception as e:
                logging.info("Creation of the directory failed")
                logging.info("Error: {}".format(e))

        if source_type == 'hs':
            try:
                res = scrape_from_hs(uri, folder_path_relative)
            except Exception as e:
                logging.info("{}".format(e))
                logging.info(
                    "Error happened scraping podcast from {}".format(source_type))
        else:
            try:
                res = scrape_from_yt(uri, folder_path_relative)
            except Exception as e:
                logging.info("{}".format(e))
                logging.info(
                    "Error happened scraping podcast from {}".format(source_type))
